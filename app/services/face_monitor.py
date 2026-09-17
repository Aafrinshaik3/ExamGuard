"""Face matching helpers. Detection can be client-side; matching uses OpenCV when available."""
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import numpy as np
from typing import List, Tuple, Optional, Dict, Any

_cv2 = None
_cv2_ok = False


def _load_cv2():
    global _cv2, _cv2_ok
    if _cv2 is not None:
        return _cv2_ok
    try:
        import cv2
        _cv2 = cv2
        _cv2_ok = hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data")
    except Exception:
        _cv2 = None
        _cv2_ok = False
    return _cv2_ok


class FacePresenceMonitor:
    def __init__(self):
        self.frontal = None
        self.frontal_alt = None
        self.profile = None
        if _load_cv2():
            base = _cv2.data.haarcascades
            self.frontal = _cv2.CascadeClassifier(base + "haarcascade_frontalface_default.xml")
            self.frontal_alt = _cv2.CascadeClassifier(base + "haarcascade_frontalface_alt2.xml")
            self.profile = _cv2.CascadeClassifier(base + "haarcascade_profileface.xml")
            if self.frontal is not None and self.frontal.empty():
                self.frontal = None

    @property
    def opencv_ready(self) -> bool:
        return _cv2_ok and self.frontal is not None

    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        if frame is None or frame.size == 0 or not self.opencv_ready:
            return []
        cv2 = _cv2
        h, w = frame.shape[:2]
        scale = 1.0
        work = frame
        if max(h, w) > 800:
            scale = 800.0 / max(h, w)
            work = cv2.resize(frame, (int(w * scale), int(h * scale)))
        gray = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        param_sets = [
            dict(scaleFactor=1.05, minNeighbors=3, minSize=(30, 30)),
            dict(scaleFactor=1.1, minNeighbors=2, minSize=(24, 24)),
            dict(scaleFactor=1.2, minNeighbors=3, minSize=(20, 20)),
        ]
        found = []
        for params in param_sets:
            for cascade in (self.frontal, self.frontal_alt):
                if cascade is None or cascade.empty():
                    continue
                for (x, y, fw, fh) in cascade.detectMultiScale(gray, **params):
                    found.append((x, y, fw, fh))
            if found:
                break
        if not found:
            return []
        inv = 1.0 / scale
        boxes = [(int(x * inv), int(y * inv), int(fw * inv), int(fh * inv)) for (x, y, fw, fh) in found]
        boxes = sorted(boxes, key=lambda b: b[2] * b[3], reverse=True)
        kept = []
        for b in boxes:
            bx, by, bw, bh = b
            overlap = False
            for kx, ky, kw, kh in kept:
                ix1, iy1 = max(bx, kx), max(by, ky)
                ix2, iy2 = min(bx + bw, kx + kw), min(by + bh, ky + kh)
                inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
                if inter > 0.3 * min(bw * bh, kw * kh):
                    overlap = True
                    break
            if not overlap:
                kept.append(b)
        return kept

    def count_faces(self, frame: np.ndarray) -> int:
        return len(self.detect_faces(frame))

    def is_present(self, frame: np.ndarray) -> bool:
        return self.count_faces(frame) >= 1

    def largest_face(self, frame: np.ndarray):
        faces = self.detect_faces(frame)
        if not faces:
            return None
        return max(faces, key=lambda f: f[2] * f[3])

    def crop_region(self, frame: np.ndarray, box: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """Crop face region; works with or without OpenCV resize."""
        x, y, w, h = [int(v) for v in box]
        pad = int(0.15 * max(w, h))
        h_img, w_img = frame.shape[:2]
        x1, y1 = max(0, x - pad), max(0, y - pad)
        x2, y2 = min(w_img, x + w + pad), min(h_img, y + h + pad)
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            return None
        if len(crop.shape) == 3:
            if _load_cv2():
                gray = _cv2.cvtColor(crop, _cv2.COLOR_BGR2GRAY)
            else:
                gray = np.mean(crop, axis=2).astype(np.uint8)
        else:
            gray = crop
        if _load_cv2():
            gray = _cv2.equalizeHist(gray)
            return _cv2.resize(gray, (120, 120))
        # numpy nearest-neighbor resize
        return self._resize_gray(gray, 120, 120)

    def _resize_gray(self, img: np.ndarray, tw: int, th: int) -> np.ndarray:
        h, w = img.shape[:2]
        ys = (np.linspace(0, h - 1, th)).astype(int)
        xs = (np.linspace(0, w - 1, tw)).astype(int)
        return img[ys][:, xs]

    def crop_face(self, frame: np.ndarray, box=None) -> Optional[np.ndarray]:
        if box is None:
            box = self.largest_face(frame)
        if box is None:
            # fallback: center square of image
            h, w = frame.shape[:2]
            side = int(min(h, w) * 0.55)
            x = (w - side) // 2
            y = (h - side) // 2
            box = (x, y, side, side)
        return self.crop_region(frame, box)

    def compare_faces(self, face_a: np.ndarray, face_b: np.ndarray) -> float:
        if face_a is None or face_b is None:
            return 0.0
        if face_a.shape != face_b.shape:
            if _load_cv2():
                face_b = _cv2.resize(face_b, (face_a.shape[1], face_a.shape[0]))
            else:
                face_b = self._resize_gray(face_b, face_a.shape[1], face_a.shape[0])
        a = face_a.astype(np.float32)
        b = face_b.astype(np.float32)
        # histogram correlation
        hist_a, _ = np.histogram(a.ravel(), bins=32, range=(0, 256), density=True)
        hist_b, _ = np.histogram(b.ravel(), bins=32, range=(0, 256), density=True)
        hist_a = hist_a / (np.linalg.norm(hist_a) + 1e-8)
        hist_b = hist_b / (np.linalg.norm(hist_b) + 1e-8)
        corr = float(np.dot(hist_a, hist_b))
        diff = float(np.mean(np.abs(a - b))) / 255.0
        diff_score = max(0.0, 1.0 - diff)
        aa = (a.ravel() - a.mean()) / (a.std() + 1e-6)
        bb = (b.ravel() - b.mean()) / (b.std() + 1e-6)
        ncc = float(np.mean(aa * bb))
        ncc_score = max(0.0, (ncc + 1.0) / 2.0)
        score = 0.35 * max(0.0, corr) + 0.30 * diff_score + 0.35 * ncc_score
        return round(min(1.0, max(0.0, score)), 4)

    def match_against_reference(
        self,
        live_frame: np.ndarray,
        reference_image_path: str,
        threshold: float = 0.30,
        client_faces: Optional[List[dict]] = None,
    ) -> Dict[str, Any]:
        result = {
            "face_present": False,
            "face_count": 0,
            "multi_face": False,
            "faces": [],
            "match": False,
            "similarity": 0.0,
            "reference_loaded": False,
            "message": "",
            "opencv_ready": self.opencv_ready,
        }

        # Prefer client-provided boxes (from browser MediaPipe) — most reliable
        faces = []
        if client_faces:
            for f in client_faces:
                try:
                    faces.append((int(f["x"]), int(f["y"]), int(f["w"]), int(f["h"])))
                except Exception:
                    pass
        if not faces:
            faces = self.detect_faces(live_frame)

        result["face_count"] = len(faces)
        result["face_present"] = len(faces) >= 1
        result["multi_face"] = len(faces) > 1
        result["faces"] = [{"x": x, "y": y, "w": w, "h": h} for (x, y, w, h) in faces]

        if not faces:
            result["message"] = "No face detected in the captured photo"
            return result
        if len(faces) > 1:
            result["message"] = "Multiple faces detected — only one person allowed"
            return result
        if not reference_image_path or not os.path.isfile(reference_image_path):
            result["message"] = "Registration photo not found — register again with a webcam photo"
            return result

        if _load_cv2():
            ref = _cv2.imread(reference_image_path)
        else:
            # fallback read via numpy if pillow not forced
            try:
                from PIL import Image
                ref = np.array(Image.open(reference_image_path).convert("RGB"))
                ref = ref[:, :, ::-1]  # RGB to BGR-ish for consistency
            except Exception:
                result["message"] = "Could not read registration photo"
                return result

        if ref is None:
            result["message"] = "Could not read registration photo"
            return result

        result["reference_loaded"] = True
        ref_face = self.crop_face(ref)  # detect or center crop
        live_face = self.crop_region(live_frame, faces[0])

        if live_face is None:
            result["message"] = "Could not crop live face"
            return result
        if ref_face is None:
            result["match"] = True
            result["similarity"] = 0.5
            result["message"] = "Registration photo unclear; presence accepted"
            return result

        sim = self.compare_faces(ref_face, live_face)
        result["similarity"] = sim
        result["match"] = sim >= threshold
        if result["match"]:
            result["message"] = f"Identity matched (score {sim:.2f})"
        else:
            result["message"] = (
                f"Identity NOT matched (score {sim:.2f}). "
                "Same person, similar lighting/angle as registration, then capture again."
            )
        return result


_monitor = None


def get_face_monitor() -> FacePresenceMonitor:
    global _monitor
    if _monitor is None:
        _monitor = FacePresenceMonitor()
    return _monitor
