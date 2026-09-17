"""Rule-based integrity scoring + violation limits for proctoring."""
from datetime import datetime
from typing import Dict, Any, List
from collections import Counter

WEIGHTS = {
    "tab_switch": 8,
    "focus_loss": 5,
    "face_absent": 10,      # per minute
    "multi_face": 15,
    "audio_spike": 6,
    "face_mismatch": 12,
}

THRESHOLDS = {
    "tab_switch": 3,
    "focus_loss": 5,
    "face_absent_seconds": 60,
    "multi_face": 1,
    "audio_spike": 4,
}

# Auto-close after this many serious violations (any type in VIOLATION_TYPES)
MAX_VIOLATIONS = 5

# Face must not disappear more than this many times
MAX_FACE_ABSENT_EVENTS = 5

# Max tab switches before hard terminate (also counts toward MAX_VIOLATIONS)
MAX_TAB_SWITCHES = 5

VIOLATION_TYPES = ("tab_switch", "multi_face", "face_absent", "face_mismatch")


def compute_integrity_score(events: List[Dict[str, Any]], session_duration_seconds: int = 3600) -> Dict[str, Any]:
    counts = Counter()
    face_absent_seconds = 0
    for ev in events:
        et = ev.get("event_type", "")
        counts[et] += 1
        if et == "face_absent":
            face_absent_seconds += int(ev.get("duration_seconds", 0))

    tabs = counts.get("tab_switch", 0)
    focus = counts.get("focus_loss", 0)
    multi = counts.get("multi_face", 0)
    audio = counts.get("audio_spike", 0)
    face_abs_events = counts.get("face_absent", 0)
    mismatch = counts.get("face_mismatch", 0)

    penalty = (
        tabs * WEIGHTS["tab_switch"]
        + focus * WEIGHTS["focus_loss"]
        + (face_absent_seconds / 60.0) * WEIGHTS["face_absent"]
        + multi * WEIGHTS["multi_face"]
        + audio * WEIGHTS["audio_spike"]
        + mismatch * WEIGHTS["face_mismatch"]
    )
    score = max(0.0, 100.0 - min(penalty, 100.0))

    ratio = 1.0
    if session_duration_seconds > 0:
        ratio = max(0.0, 1.0 - face_absent_seconds / session_duration_seconds)

    if score >= 70:
        risk = "Low"
    elif score >= 40:
        risk = "Medium"
    else:
        risk = "High"

    flagged = []
    if tabs >= MAX_TAB_SWITCHES:
        flagged.append(f"Tab switches reached limit ({tabs})")
    elif tabs > THRESHOLDS["tab_switch"]:
        flagged.append(f"Excessive tab switches ({tabs})")
    if face_abs_events >= MAX_FACE_ABSENT_EVENTS:
        flagged.append(f"Face absent events reached limit ({face_abs_events})")
    if face_absent_seconds > THRESHOLDS["face_absent_seconds"]:
        flagged.append(f"Face absent total {face_absent_seconds}s")
    if multi >= THRESHOLDS["multi_face"]:
        flagged.append(f"Multiple faces ({multi})")
    if audio > THRESHOLDS["audio_spike"]:
        flagged.append(f"Suspicious audio spikes ({audio})")
    if mismatch:
        flagged.append(f"Identity mismatches ({mismatch})")

    return {
        "score": round(score, 2),
        "risk_label": risk,
        "tab_switch_count": tabs,
        "focus_loss_count": focus,
        "face_absent_seconds": face_absent_seconds,
        "face_absent_events": face_abs_events,
        "multi_face_count": multi,
        "audio_spike_count": audio,
        "face_presence_ratio": round(ratio, 4),
        "flagged_reasons": flagged,
        "computed_at": datetime.utcnow().isoformat(),
    }
