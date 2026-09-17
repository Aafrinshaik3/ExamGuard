"""Analytics data helpers for the embedded admin dashboard (no Streamlit required).

Provides every view that the Streamlit dashboard used to offer:
Overview · All students · Scores · Events · Clustering · Risk · Drill-down · Exports
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func

from app import db
from app.models.models import (
    AIReport,
    AvailableExam,
    EventLog,
    ExamSession,
    IntegrityScore,
    User,
)


def _category_from_exam(title: str, subject: Optional[str]) -> str:
    """Derive a human-friendly category label similar to the Streamlit view."""
    t = (title or "").lower()
    s = (subject or "").lower()
    if "banking" in t or "banking" in s or "quantitative" in t or "aptitude" in t:
        return "Banking Exams"
    if (
        "coding" in t
        or "programming" in t
        or "data structures" in t
        or "networks" in t
        or "python" in t
        or "machine learning" in t
        or "database" in t
        or "dbms" in t
    ):
        return "Coding Exams — IT"
    if "aptitude" in t or "quantitative" in t or "general" in s:
        return "General Aptitude"
    if subject and subject not in ("General", "All"):
        return subject
    if title:
        return title.split(":")[0].strip()[:40] or "Other"
    return "Other"


def _difficulty_from_exam(title: str, duration: Optional[int], total_q: Optional[int]) -> str:
    t = (title or "").lower()
    if "beginner" in t or "foundation" in t or "basics" in t:
        return "Easy"
    if "advanced" in t or "final" in t:
        return "Hard"
    return "Medium"


def _safe_float(val) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if s in ("", "None", "none", "null"):
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _load_session_rows() -> List[Dict[str, Any]]:
    """Join sessions + users + integrity + available exam into flat dicts."""
    rows = (
        db.session.query(
            ExamSession.id.label("session_id"),
            ExamSession.candidate_id,
            User.full_name.label("candidate_name"),
            User.email.label("candidate_email"),
            ExamSession.exam_title,
            ExamSession.status,
            ExamSession.test_score,
            ExamSession.started_at,
            ExamSession.ended_at,
            ExamSession.duration_minutes,
            ExamSession.created_at,
            IntegrityScore.score.label("integrity_score"),
            IntegrityScore.risk_label,
            IntegrityScore.tab_switch_count,
            IntegrityScore.focus_loss_count,
            IntegrityScore.face_absent_seconds,
            IntegrityScore.multi_face_count,
            IntegrityScore.audio_spike_count,
            IntegrityScore.face_presence_ratio,
            AvailableExam.subject,
            AvailableExam.duration_minutes.label("exam_duration"),
            AvailableExam.total_questions,
        )
        .outerjoin(User, User.id == ExamSession.candidate_id)
        .outerjoin(IntegrityScore, IntegrityScore.session_id == ExamSession.id)
        .outerjoin(AvailableExam, AvailableExam.id == ExamSession.exam_id)
        .order_by(ExamSession.id.desc())
        .all()
    )

    attempts: List[Dict[str, Any]] = []
    for r in rows:
        cat = _category_from_exam(r.exam_title or "", r.subject)
        diff = _difficulty_from_exam(r.exam_title or "", r.exam_duration, r.total_questions)

        test_score_val = _safe_float(r.test_score)
        integrity_val = _safe_float(r.integrity_score)
        # Prefer exam mark when present; else integrity score (for charts)
        display_score = test_score_val if test_score_val is not None else integrity_val

        attempts.append(
            {
                "session_id": r.session_id,
                "candidate_id": r.candidate_id,
                "candidate_name": r.candidate_name or "—",
                "candidate_email": r.candidate_email or "",
                "exam_title": r.exam_title or "—",
                "category": cat,
                "difficulty": diff,
                "status": r.status or "—",
                "test_score": test_score_val,
                "integrity_score": integrity_val,
                "display_score": display_score,
                "risk_label": r.risk_label,
                "tab_switch_count": r.tab_switch_count or 0,
                "focus_loss_count": r.focus_loss_count or 0,
                "face_absent_seconds": r.face_absent_seconds or 0,
                "multi_face_count": r.multi_face_count or 0,
                "audio_spike_count": r.audio_spike_count or 0,
                "face_presence_ratio": float(r.face_presence_ratio)
                if r.face_presence_ratio is not None
                else 1.0,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "ended_at": r.ended_at.isoformat() if r.ended_at else None,
                "duration_minutes": r.duration_minutes or 0,
            }
        )
    return attempts


def load_analytics_overview() -> Dict[str, Any]:
    """Load data for the Overview page (matches Streamlit screenshot layout)."""
    attempts = _load_session_rows()

    risk_counts = {"High": 0, "Medium": 0, "Low": 0}
    category_scores: Dict[str, List[float]] = defaultdict(list)

    for a in attempts:
        if a["risk_label"] in risk_counts:
            risk_counts[a["risk_label"]] += 1
        if a["display_score"] is not None:
            category_scores[a["category"]].append(a["display_score"])

    total_risk = sum(risk_counts.values()) or 1
    # Order matches screenshot legend: High (red), Low (green), Medium (orange)
    risk_distribution = {
        "labels": ["High", "Low", "Medium"],
        "values": [risk_counts["High"], risk_counts["Low"], risk_counts["Medium"]],
        "percents": [
            round(100.0 * risk_counts["High"] / total_risk, 1),
            round(100.0 * risk_counts["Low"] / total_risk, 1),
            round(100.0 * risk_counts["Medium"] / total_risk, 1),
        ],
        "colors": ["#dc2626", "#16a34a", "#d97706"],
    }

    avg_by_category = []
    for cat, scores in sorted(category_scores.items(), key=lambda x: x[0]):
        if scores:
            avg_by_category.append(
                {
                    "category": cat,
                    "avg_score": round(sum(scores) / len(scores), 1),
                    "n": len(scores),
                }
            )

    scored = [a for a in attempts if a["integrity_score"] is not None]
    avg_integrity = (
        round(sum(a["integrity_score"] for a in scored) / len(scored), 1) if scored else 0.0
    )
    high_risk = risk_counts["High"]
    unique_students = len(
        {a["candidate_id"] for a in attempts if a["candidate_id"] is not None}
    )

    return {
        "total_attempts": len(attempts),
        "unique_students": unique_students,
        "scored_sessions": len(scored),
        "avg_integrity": avg_integrity,
        "high_risk_count": high_risk,
        "risk_distribution": risk_distribution,
        "avg_by_category": avg_by_category,
        "latest_attempts": attempts[:40],
        "all_attempts": attempts,
    }


def load_all_students_data() -> Dict[str, Any]:
    """Per-student summary + full session list."""
    attempts = _load_session_rows()
    by_student: Dict[Any, Dict[str, Any]] = {}

    for a in attempts:
        cid = a["candidate_id"]
        if cid is None:
            continue
        if cid not in by_student:
            by_student[cid] = {
                "candidate_id": cid,
                "candidate_name": a["candidate_name"],
                "candidate_email": a["candidate_email"],
                "attempts": 0,
                "scores": [],
                "exams": set(),
                "tab_switches": 0,
                "face_absent_seconds": 0,
            }
        s = by_student[cid]
        s["attempts"] += 1
        if a["integrity_score"] is not None:
            s["scores"].append(a["integrity_score"])
        if a["exam_title"] and a["exam_title"] != "—":
            s["exams"].add(a["exam_title"])
        s["tab_switches"] += a["tab_switch_count"]
        s["face_absent_seconds"] += a["face_absent_seconds"]

    student_summary = []
    for s in by_student.values():
        student_summary.append(
            {
                "candidate_id": s["candidate_id"],
                "candidate_name": s["candidate_name"],
                "candidate_email": s["candidate_email"],
                "attempts": s["attempts"],
                "avg_score": round(sum(s["scores"]) / len(s["scores"]), 1)
                if s["scores"]
                else None,
                "exams": ", ".join(sorted(s["exams"])) or "—",
                "tab_switches": s["tab_switches"],
                "face_absent_seconds": s["face_absent_seconds"],
            }
        )
    student_summary.sort(key=lambda x: x["attempts"], reverse=True)

    return {
        "student_summary": student_summary,
        "all_attempts": attempts,
        "total_sessions": len(attempts),
        "unique_students": len(student_summary),
    }


def load_scores_data() -> Dict[str, Any]:
    """Integrity score distributions for charts."""
    attempts = _load_session_rows()
    scored = [a for a in attempts if a["integrity_score"] is not None]

    # Histogram bins (0-100, step 10)
    bins = list(range(0, 101, 10))
    hist_counts = [0] * (len(bins) - 1)
    for a in scored:
        sc = a["integrity_score"]
        idx = min(int(sc // 10), len(hist_counts) - 1)
        if idx < 0:
            idx = 0
        hist_counts[idx] += 1

    by_risk = {"Low": [], "Medium": [], "High": []}
    for a in scored:
        if a["risk_label"] in by_risk:
            by_risk[a["risk_label"]].append(a["integrity_score"])

    scatter = [
        {
            "session_id": a["session_id"],
            "candidate_name": a["candidate_name"],
            "exam_title": a["exam_title"],
            "x": a["tab_switch_count"],
            "y": a["integrity_score"],
            "size": max(5, min(40, (a["face_absent_seconds"] or 0) / 10 + 5)),
            "risk": a["risk_label"] or "Low",
        }
        for a in scored
    ]

    return {
        "scored": scored,
        "hist_labels": [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)],
        "hist_counts": hist_counts,
        "box_by_risk": {
            "Low": by_risk["Low"],
            "Medium": by_risk["Medium"],
            "High": by_risk["High"],
        },
        "scatter": scatter,
        "avg_score": round(sum(a["integrity_score"] for a in scored) / len(scored), 1)
        if scored
        else 0.0,
    }


def load_events_data() -> Dict[str, Any]:
    """Event type counts, recent events, flagged total."""
    events = (
        EventLog.query.order_by(EventLog.timestamp.desc()).limit(500).all()
    )
    type_counts: Counter = Counter()
    flagged = 0
    day_type: Dict[str, Counter] = defaultdict(Counter)
    rows = []

    for e in events:
        type_counts[e.event_type] += 1
        if e.is_flagged:
            flagged += 1
        day = e.timestamp.strftime("%Y-%m-%d") if e.timestamp else "unknown"
        day_type[day][e.event_type] += 1
        rows.append(
            {
                "id": e.id,
                "session_id": e.session_id,
                "event_type": e.event_type,
                "severity": e.severity or "info",
                "timestamp": e.timestamp.isoformat() if e.timestamp else "",
                "duration_seconds": e.duration_seconds or 0,
                "details": (e.details or "")[:120],
                "is_flagged": bool(e.is_flagged),
            }
        )

    # Top event types for bar chart
    sorted_types = type_counts.most_common(12)
    event_type_labels = [t for t, _ in sorted_types]
    event_type_values = [c for _, c in sorted_types]

    # Simple day heatmap data (last 14 days with activity)
    days_sorted = sorted(day_type.keys())[-14:]
    all_types = sorted({t for day in days_sorted for t in day_type[day]})
    heatmap = {
        "days": days_sorted,
        "types": all_types,
        "matrix": [
            [day_type[d].get(t, 0) for d in days_sorted] for t in all_types
        ],
    }

    return {
        "event_type_labels": event_type_labels,
        "event_type_values": event_type_values,
        "flagged_count": flagged,
        "total_events": len(rows),
        "recent_events": rows[:100],
        "heatmap": heatmap,
    }


def load_clustering_data(k: int = 3) -> Dict[str, Any]:
    """K-Means behaviour clustering on scored sessions."""
    attempts = _load_session_rows()
    scored = [a for a in attempts if a["integrity_score"] is not None]

    if len(scored) < 2:
        return {
            "ok": False,
            "message": "Need at least 2 scored sessions to run clustering.",
            "k": k,
            "points": [],
            "summary": [],
            "cluster_labels": {},
        }

    try:
        import numpy as np
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        return {
            "ok": False,
            "message": "scikit-learn is required for clustering.",
            "k": k,
            "points": [],
            "summary": [],
            "cluster_labels": {},
        }

    feats = [
        "tab_switch_count",
        "focus_loss_count",
        "face_absent_seconds",
        "multi_face_count",
        "face_presence_ratio",
        "audio_spike_count",
    ]
    X = np.array([[float(a.get(f) or 0) for f in feats] for a in scored], dtype=float)
    X = StandardScaler().fit_transform(X)

    k = max(2, min(k, len(scored), 5))
    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)

    # Attach clusters
    for i, a in enumerate(scored):
        a["cluster"] = int(labels[i])

    # Cluster averages
    summary_rows = []
    cluster_labels_map: Dict[int, str] = {}
    for c in range(k):
        members = [a for a in scored if a["cluster"] == c]
        if not members:
            continue
        avg_tabs = sum(m["tab_switch_count"] for m in members) / len(members)
        avg_face = sum(m["face_absent_seconds"] for m in members) / len(members)
        avg_score = sum(m["integrity_score"] for m in members) / len(members)
        avg_focus = sum(m["focus_loss_count"] for m in members) / len(members)
        avg_multi = sum(m["multi_face_count"] for m in members) / len(members)
        avg_audio = sum(m["audio_spike_count"] for m in members) / len(members)
        avg_ratio = sum(m["face_presence_ratio"] for m in members) / len(members)

        if avg_tabs <= 1 and avg_face <= 30:
            profile = "Clean / focused"
        elif avg_tabs >= 4 or avg_face >= 120:
            profile = "High distraction / risk"
        else:
            profile = "Moderate issues"
        cluster_labels_map[c] = profile

        summary_rows.append(
            {
                "cluster": c,
                "profile": profile,
                "n": len(members),
                "avg_score": round(avg_score, 1),
                "avg_tab_switch": round(avg_tabs, 1),
                "avg_face_absent_s": round(avg_face, 1),
                "avg_focus_loss": round(avg_focus, 1),
                "avg_multi_face": round(avg_multi, 1),
                "avg_audio_spike": round(avg_audio, 1),
                "avg_face_ratio": round(avg_ratio, 3),
            }
        )

    points = [
        {
            "session_id": a["session_id"],
            "candidate_name": a["candidate_name"],
            "exam_title": a["exam_title"],
            "cluster": a["cluster"],
            "profile": cluster_labels_map.get(a["cluster"], "—"),
            "tab_switch_count": a["tab_switch_count"],
            "face_absent_seconds": a["face_absent_seconds"],
            "score": a["integrity_score"],
            "risk_label": a["risk_label"],
        }
        for a in scored
    ]

    return {
        "ok": True,
        "k": k,
        "points": points,
        "summary": summary_rows,
        "cluster_labels": {str(k_): v for k_, v in cluster_labels_map.items()},
        "message": None,
    }


def load_risk_data() -> Dict[str, Any]:
    """Risk profiling page."""
    attempts = _load_session_rows()
    scored = [a for a in attempts if a["risk_label"]]
    order = ["Low", "Medium", "High"]
    counts = {r: 0 for r in order}
    for a in scored:
        if a["risk_label"] in counts:
            counts[a["risk_label"]] += 1

    high = sorted(
        [a for a in scored if a["risk_label"] == "High"],
        key=lambda x: (x["integrity_score"] is None, x["integrity_score"] or 0),
    )

    return {
        "risk_labels": order,
        "risk_counts": [counts[r] for r in order],
        "risk_colors": ["#16a34a", "#d97706", "#dc2626"],
        "high_risk_sessions": high[:50],
        "total_scored": len(scored),
    }


def load_drilldown_data(session_id: Optional[int] = None) -> Dict[str, Any]:
    """Single-session drill-down with AI report + events."""
    attempts = _load_session_rows()
    session_ids = [a["session_id"] for a in attempts]

    selected = None
    if session_id is not None:
        selected = next((a for a in attempts if a["session_id"] == session_id), None)
    if selected is None and attempts:
        selected = attempts[0]
        session_id = selected["session_id"]

    ai_text = None
    model_used = None
    if session_id is not None:
        report = AIReport.query.filter_by(session_id=session_id).first()
        if report:
            ai_text = report.summary_text
            model_used = report.model_used

        events = (
            EventLog.query.filter_by(session_id=session_id)
            .order_by(EventLog.timestamp.asc())
            .all()
        )
        event_rows = [
            {
                "event_type": e.event_type,
                "severity": e.severity,
                "timestamp": e.timestamp.isoformat() if e.timestamp else "",
                "duration_seconds": e.duration_seconds or 0,
                "details": e.details or "",
                "is_flagged": bool(e.is_flagged),
            }
            for e in events
        ]
    else:
        event_rows = []

    return {
        "session_ids": session_ids[:200],
        "selected": selected,
        "selected_id": session_id,
        "ai_summary": ai_text,
        "model_used": model_used,
        "events": event_rows,
    }


def load_exports_meta() -> Dict[str, Any]:
    """File presence + row counts for export page."""
    from pathlib import Path
    from flask import current_app

    root = Path(current_app.root_path).parent
    export_dir = root / "data" / "exports"
    files = {}
    for name in (
        "integrity_scores.csv",
        "session_logs.csv",
        "ai_reports.json",
        "cluster_assignments.csv",
    ):
        p = export_dir / name
        files[name] = {
            "exists": p.exists(),
            "size": p.stat().st_size if p.exists() else 0,
            "path": str(p),
        }
    return {"files": files, "export_dir": str(export_dir)}
