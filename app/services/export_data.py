"""Export all real exam sessions from SQLite to analytics CSV/JSON files."""
import json
import os
from pathlib import Path


def export_analytics_data(app=None):
    """
    Read every session / score / event / AI report from the live DB
    and write data/exports/*.csv|json so Streamlit (and downloads) stay current.
    """
    from flask import current_app
    from app import db
    from app.models.models import (
        ExamSession, IntegrityScore, EventLog, AIReport, User
    )

    if app is not None:
        ctx = app.app_context()
        ctx.push()
    else:
        ctx = None

    try:
        root = Path(current_app.root_path).parent
        export_dir = root / "data" / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)

        # ---- integrity_scores.csv (one row per scored session) ----
        score_rows = []
        sessions = ExamSession.query.order_by(ExamSession.created_at.desc()).all()
        for s in sessions:
            cand = s.candidate
            name = cand.full_name if cand else "Unknown"
            email = cand.email if cand else ""
            sc = s.integrity_score
            row = {
                "session_id": s.id,
                "candidate_id": s.candidate_id,
                "candidate_name": name,
                "candidate_email": email,
                "exam_title": s.exam_title or "",
                "status": s.status or "",
                "started_at": s.started_at.isoformat() if s.started_at else "",
                "ended_at": s.ended_at.isoformat() if s.ended_at else "",
                "duration_minutes": s.duration_minutes or 0,
                "score": sc.score if sc else None,
                "risk_label": sc.risk_label if sc else "",
                "tab_switch_count": sc.tab_switch_count if sc else 0,
                "focus_loss_count": sc.focus_loss_count if sc else 0,
                "face_absent_seconds": sc.face_absent_seconds if sc else 0,
                "multi_face_count": sc.multi_face_count if sc else 0,
                "audio_spike_count": (sc.audio_spike_count if sc else 0) or 0,
                "face_presence_ratio": sc.face_presence_ratio if sc else 1.0,
            }
            score_rows.append(row)

        import pandas as pd
        pd.DataFrame(score_rows).to_csv(export_dir / "integrity_scores.csv", index=False)

        # ---- session_logs.csv (all events) ----
        event_rows = []
        for e in EventLog.query.order_by(EventLog.timestamp.asc()).all():
            event_rows.append({
                "id": e.id,
                "session_id": e.session_id,
                "event_type": e.event_type,
                "severity": e.severity,
                "timestamp": e.timestamp.isoformat() if e.timestamp else "",
                "duration_seconds": e.duration_seconds or 0,
                "details": e.details or "",
                "is_flagged": bool(e.is_flagged),
            })
        pd.DataFrame(event_rows).to_csv(export_dir / "session_logs.csv", index=False)

        # ---- ai_reports.json ----
        ai_rows = []
        for r in AIReport.query.all():
            ai_rows.append({
                "session_id": r.session_id,
                "summary_text": r.summary_text,
                "model_used": r.model_used,
                "generated_at": r.generated_at.isoformat() if r.generated_at else "",
            })
        with open(export_dir / "ai_reports.json", "w") as f:
            json.dump(ai_rows, f, indent=2)

        return {
            "sessions": len(score_rows),
            "events": len(event_rows),
            "reports": len(ai_rows),
            "export_dir": str(export_dir),
        }
    finally:
        if ctx is not None:
            ctx.pop()
