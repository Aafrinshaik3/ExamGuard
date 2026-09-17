"""Event logging, face-detect, face-verify APIs."""
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.models import ExamSession, EventLog
from app.services.face_monitor import get_face_monitor
from app.services.scoring import THRESHOLDS, MAX_VIOLATIONS, MAX_FACE_ABSENT_EVENTS, MAX_TAB_SWITCHES, VIOLATION_TYPES
import base64
import numpy as np

api_bp = Blueprint("api", __name__)


def _decode_image(image_b64: str):
    if not image_b64:
        return None
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]
    try:
        raw = base64.b64decode(image_b64)
        arr = np.frombuffer(raw, np.uint8)
        try:
            import cv2
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is not None:
                return frame
        except Exception:
            pass
        from io import BytesIO
        from PIL import Image
        img = Image.open(BytesIO(raw))
        rgb = np.array(img.convert("RGB"))
        return rgb[:, :, ::-1].copy()
    except Exception:
        return None


def _resolve_registration_photo():
    rel = (current_user.photo_path or "").replace("\\", "/").strip()
    if not rel:
        return None
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    project_static = os.path.join(project_root, "static")
    upload_folder = current_app.config.get("UPLOAD_FOLDER") or os.path.join(project_static, "uploads")
    basename = os.path.basename(rel)
    candidates = [
        os.path.join(project_static, rel),
        os.path.join(project_root, "static", rel),
        os.path.join(upload_folder, rel),
        os.path.join(upload_folder, "photos", basename),
        os.path.join(upload_folder, basename),
        os.path.join(project_static, "uploads", "photos", basename),
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def _violation_count(session_id: int) -> int:
    return EventLog.query.filter(
        EventLog.session_id == session_id,
        EventLog.event_type.in_(VIOLATION_TYPES),
    ).count()


def _face_absent_count(session_id: int) -> int:
    return EventLog.query.filter_by(session_id=session_id, event_type="face_absent").count()


def _tab_switch_count(session_id: int) -> int:
    return EventLog.query.filter_by(session_id=session_id, event_type="tab_switch").count()


def _maybe_terminate(session: ExamSession, vcount: int) -> bool:
    """Terminate on total violations, 5 face-absent events, or 5 tab switches."""
    if session.status != "active":
        return session.status == "terminated"
    face_n = _face_absent_count(session.id)
    tab_n = _tab_switch_count(session.id)
    if vcount >= MAX_VIOLATIONS or face_n >= MAX_FACE_ABSENT_EVENTS or tab_n >= MAX_TAB_SWITCHES:
        session.status = "terminated"
        session.ended_at = datetime.utcnow()
        db.session.commit()
        return True
    return False


@api_bp.route("/face-detect", methods=["POST"])
@login_required
def face_detect():
    """Server-side detection (optional). Client MediaPipe is primary."""
    data = request.get_json() or {}
    image_b64 = data.get("image")
    if not image_b64:
        return jsonify({"error": "image required", "face_present": False, "faces": []}), 400
    try:
        frame = _decode_image(image_b64)
        if frame is None:
            return jsonify({"error": "decode failed", "face_present": False, "faces": []}), 400
        monitor = get_face_monitor()
        faces = monitor.detect_faces(frame)
        return jsonify({
            "face_present": len(faces) >= 1,
            "face_count": len(faces),
            "multi_face": len(faces) > 1,
            "faces": [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces],
            "opencv_ready": monitor.opencv_ready,
        })
    except Exception as e:
        return jsonify({"error": str(e), "face_present": False, "faces": [], "opencv_ready": False}), 200


@api_bp.route("/face-verify", methods=["POST"])
@login_required
def face_verify():
    """Compare captured snapshot to registration photo. Accepts client face boxes."""
    data = request.get_json() or {}
    image_b64 = data.get("image")
    client_faces = data.get("faces") or []
    if not image_b64:
        return jsonify({"error": "image required"}), 400

    try:
        frame = _decode_image(image_b64)
        if frame is None:
            return jsonify({"error": "Could not decode image"}), 400

        monitor = get_face_monitor()

        # If client sent boxes, trust them for presence
        if client_faces:
            faces_list = []
            for f in client_faces:
                try:
                    faces_list.append({
                        "x": int(f["x"]), "y": int(f["y"]),
                        "w": int(f["w"]), "h": int(f["h"]),
                    })
                except Exception:
                    pass
            if not faces_list:
                return jsonify({
                    "verified": False, "similarity": 0.0,
                    "message": "No face in capture",
                    "face_present": False, "face_count": 0, "multi_face": False, "faces": [],
                })
            if len(faces_list) > 1:
                return jsonify({
                    "verified": False, "similarity": 0.0,
                    "message": "Multiple faces — only you should be in frame",
                    "face_present": True, "face_count": len(faces_list), "multi_face": True,
                    "faces": faces_list,
                })
        else:
            faces_list = None

        if not current_user.photo_path:
            return jsonify({
                "verified": False, "similarity": 0.0,
                "message": "No registration photo. Register again and capture a face photo.",
                "face_present": bool(client_faces), "face_count": len(client_faces or []),
                "multi_face": False, "faces": client_faces or [],
            })

        ref_path = _resolve_registration_photo()
        if not ref_path:
            return jsonify({
                "verified": False, "similarity": 0.0,
                "message": "Registration photo file missing. Register again with a webcam photo.",
                "face_present": bool(client_faces), "face_count": len(client_faces or []),
                "multi_face": False, "faces": client_faces or [],
            })

        match_result = monitor.match_against_reference(
            frame, ref_path, client_faces=client_faces or None
        )
        return jsonify({
            "verified": bool(match_result["match"]),
            "similarity": match_result["similarity"],
            "message": match_result["message"],
            "face_present": match_result["face_present"],
            "face_count": match_result["face_count"],
            "multi_face": match_result["multi_face"],
            "faces": match_result["faces"],
            "opencv_ready": match_result.get("opencv_ready", False),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/event", methods=["POST"])
@login_required
def log_event():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    event_type = data.get("event_type")
    duration = int(data.get("duration_seconds", 0))
    details = data.get("details", "")

    if not session_id or not event_type:
        return jsonify({"error": "session_id and event_type required"}), 400

    session = ExamSession.query.get(session_id)
    if not session or (
        session.candidate_id != current_user.id
        and current_user.role not in ("invigilator", "admin")
    ):
        return jsonify({"error": "Unauthorized"}), 403

    if session.status != "active":
        return jsonify({"error": "Session not active", "force_close": True, "status": session.status}), 400

    is_flagged = event_type in ("tab_switch", "multi_face", "face_absent", "face_mismatch")
    severity = "warning"
    if event_type in ("face_absent", "multi_face", "face_mismatch"):
        severity = "critical"
    elif event_type == "focus_loss":
        c = EventLog.query.filter_by(session_id=session_id, event_type="focus_loss").count() + 1
        is_flagged = c > THRESHOLDS["focus_loss"]
    elif event_type == "audio_spike":
        c = EventLog.query.filter_by(session_id=session_id, event_type="audio_spike").count() + 1
        is_flagged = c > THRESHOLDS["audio_spike"]

    event = EventLog(
        session_id=session_id, event_type=event_type, severity=severity,
        duration_seconds=duration, details=details, is_flagged=is_flagged,
        timestamp=datetime.utcnow(),
    )
    db.session.add(event)
    db.session.commit()

    vcount = _violation_count(session_id)
    force_close = _maybe_terminate(session, vcount)
    face_n = _face_absent_count(session_id)
    tab_n = _tab_switch_count(session_id)
    return jsonify({
        "id": event.id,
        "is_flagged": is_flagged,
        "severity": severity,
        "violation_count": vcount,
        "max_violations": MAX_VIOLATIONS,
        "face_absent_count": face_n,
        "max_face_absent": MAX_FACE_ABSENT_EVENTS,
        "tab_switch_count": tab_n,
        "max_tab_switches": MAX_TAB_SWITCHES,
        "force_close": force_close,
        "remaining": max(0, MAX_VIOLATIONS - vcount),
        "remaining_face": max(0, MAX_FACE_ABSENT_EVENTS - face_n),
        "remaining_tabs": max(0, MAX_TAB_SWITCHES - tab_n),
    })


@api_bp.route("/face-check", methods=["POST"])
@login_required
def face_check():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    image_b64 = data.get("image")
    client_faces = data.get("faces") or []
    check_match = bool(data.get("check_match", False))

    if not image_b64 and not client_faces:
        return jsonify({"error": "image or faces required"}), 400
    try:
        faces = []
        if client_faces:
            faces = [(int(f["x"]), int(f["y"]), int(f["w"]), int(f["h"])) for f in client_faces]
        elif image_b64:
            frame = _decode_image(image_b64)
            if frame is not None:
                faces = get_face_monitor().detect_faces(frame)

        count = len(faces)
        result = {
            "face_present": count >= 1,
            "face_count": count,
            "multi_face": count > 1,
            "faces": [{"x": x, "y": y, "w": w, "h": h} for (x, y, w, h) in faces],
            "match": None,
            "similarity": None,
        }

        if check_match and image_b64 and current_user.photo_path and count == 1:
            frame = _decode_image(image_b64)
            ref = _resolve_registration_photo()
            if frame is not None and ref:
                mr = get_face_monitor().match_against_reference(frame, ref, client_faces=client_faces)
                result["match"] = mr["match"]
                result["similarity"] = mr["similarity"]
                result["match_message"] = mr["message"]

        if count > 1 and session_id:
            session = ExamSession.query.get(session_id)
            if session and session.candidate_id == current_user.id and session.status == "active":
                db.session.add(EventLog(
                    session_id=session_id, event_type="multi_face", severity="critical",
                    is_flagged=True, details=f"{count} faces", timestamp=datetime.utcnow(),
                ))
                db.session.commit()
                vcount = _violation_count(session_id)
                result["violation_count"] = vcount
                result["force_close"] = _maybe_terminate(session, vcount)

        if session_id:
            session = ExamSession.query.get(session_id)
            if session and session.status != "active":
                result["force_close"] = True
                result["session_status"] = session.status
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
