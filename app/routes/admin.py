"""Admin and Invigilator Console routes for ExamGuard."""
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, jsonify, current_app
)
from flask_login import login_required, current_user
from app import db
from app.models.models import (
    User, ExamSession, EventLog, IntegrityScore, AIReport, AvailableExam
)
from app.services.scoring import MAX_VIOLATIONS, VIOLATION_TYPES
from app.services.export_data import export_analytics_data

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role not in ("invigilator", "admin"):
            flash("Invigilator or Admin access required.", "danger")
            return redirect(url_for("exam.candidate_home"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/admin")
@admin_bp.route("/invigilator")
@admin_required
def dashboard():
    """Main overview dashboard with summary KPIs and recent activity."""
    total_students = User.query.filter_by(role="candidate").count()
    total_sessions = ExamSession.query.count()
    active_sessions_count = ExamSession.query.filter_by(status="active").count()
    attended_sessions = ExamSession.query.filter(
        ExamSession.status.in_(["submitted", "terminated"])
    ).count()

    # Risk metrics
    low_risk = IntegrityScore.query.filter_by(risk_label="Low").count()
    med_risk = IntegrityScore.query.filter_by(risk_label="Medium").count()
    high_risk = IntegrityScore.query.filter_by(risk_label="High").count()

    # Average score
    avg_score_raw = db.session.query(db.func.avg(IntegrityScore.score)).scalar()
    avg_score = round(float(avg_score_raw), 1) if avg_score_raw is not None else 0.0

    # Violation counts
    audio_spikes = EventLog.query.filter_by(event_type="audio_spike").count()
    face_absences = EventLog.query.filter_by(event_type="face_absent").count()
    tab_switches = EventLog.query.filter_by(event_type="tab_switch").count()
    multi_faces = EventLog.query.filter_by(event_type="multi_face").count()
    focus_losses = EventLog.query.filter_by(event_type="focus_loss").count()

    # Active and recent sessions
    active_sessions = (
        ExamSession.query.filter_by(status="active")
        .order_by(ExamSession.started_at.desc())
        .limit(10)
        .all()
    )
    recent_sessions = (
        ExamSession.query.order_by(ExamSession.created_at.desc())
        .limit(20)
        .all()
    )

    # Invigilators and faculty members
    invigilators = (
        User.query.filter(User.role.in_(["invigilator", "admin"]))
        .order_by(User.created_at.desc())
        .all()
    )

    stats = {
        "total_students": total_students,
        "total_invigilators": len(invigilators),
        "total_sessions": total_sessions,
        "active_sessions": active_sessions_count,
        "attended_sessions": attended_sessions,
        "low_risk": low_risk,
        "med_risk": med_risk,
        "high_risk": high_risk,
        "avg_score": avg_score,
        "audio_spikes": audio_spikes,
        "face_absences": face_absences,
        "tab_switches": tab_switches,
        "multi_faces": multi_faces,
        "focus_losses": focus_losses,
    }

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        invigilators=invigilators,
        active_sessions=active_sessions,
        recent_sessions=recent_sessions,
    )


@admin_bp.route("/admin/live")
@admin_required
def live_proctor():
    """Live proctoring console: real-time monitoring of student face and voice."""
    active_sessions = (
        ExamSession.query.filter_by(status="active")
        .order_by(ExamSession.started_at.desc())
        .all()
    )
    return render_template("admin/live_proctor.html", active_sessions=active_sessions)


@admin_bp.route("/api/admin/live-feed")
@admin_required
def api_live_feed():
    """Real-time polling endpoint for live student face and voice tracking."""
    active_sessions = (
        ExamSession.query.filter_by(status="active")
        .order_by(ExamSession.started_at.desc())
        .all()
    )

    now = datetime.utcnow()
    recent_cutoff = now - timedelta(seconds=20)

    sessions_data = []
    for s in active_sessions:
        candidate = s.candidate
        elapsed_sec = 0
        if s.started_at:
            elapsed_sec = max(0, int((now - s.started_at).total_seconds()))

        # Counts
        tabs = EventLog.query.filter_by(session_id=s.id, event_type="tab_switch").count()
        focus = EventLog.query.filter_by(session_id=s.id, event_type="focus_loss").count()
        face_abs = EventLog.query.filter_by(session_id=s.id, event_type="face_absent").count()
        multi_face = EventLog.query.filter_by(session_id=s.id, event_type="multi_face").count()
        audio_spikes = EventLog.query.filter_by(session_id=s.id, event_type="audio_spike").count()
        total_v = EventLog.query.filter(
            EventLog.session_id == s.id,
            EventLog.event_type.in_(VIOLATION_TYPES),
        ).count()

        # Recent events for live warning pills
        recent_audio = EventLog.query.filter(
            EventLog.session_id == s.id,
            EventLog.event_type == "audio_spike",
            EventLog.timestamp >= recent_cutoff,
        ).first()

        recent_face_absent = EventLog.query.filter(
            EventLog.session_id == s.id,
            EventLog.event_type == "face_absent",
            EventLog.timestamp >= recent_cutoff,
        ).first()

        recent_multi_face = EventLog.query.filter(
            EventLog.session_id == s.id,
            EventLog.event_type == "multi_face",
            EventLog.timestamp >= recent_cutoff,
        ).first()

        recent_tab = EventLog.query.filter(
            EventLog.session_id == s.id,
            EventLog.event_type == "tab_switch",
            EventLog.timestamp >= recent_cutoff,
        ).first()

        # Latest single event
        latest_ev = (
            EventLog.query.filter_by(session_id=s.id)
            .order_by(EventLog.timestamp.desc())
            .first()
        )

        sessions_data.append({
            "session_id": s.id,
            "candidate_id": s.candidate_id,
            "candidate_name": candidate.full_name if candidate else "Unknown Candidate",
            "candidate_email": candidate.email if candidate else "",
            "candidate_photo": candidate.photo_path if candidate and candidate.photo_path else None,
            "exam_title": s.exam_title,
            "duration_minutes": s.duration_minutes,
            "elapsed_seconds": elapsed_sec,
            "elapsed_formatted": f"{elapsed_sec // 60:02d}:{elapsed_sec % 60:02d}",
            "tab_switch_count": tabs,
            "focus_loss_count": focus,
            "face_absent_count": face_abs,
            "multi_face_count": multi_face,
            "audio_spike_count": audio_spikes,
            "violation_count": total_v,
            "max_violations": MAX_VIOLATIONS,
            "audio_spike_active": bool(recent_audio),
            "face_absent_active": bool(recent_face_absent),
            "multi_face_active": bool(recent_multi_face),
            "tab_switch_active": bool(recent_tab),
            "latest_event_type": latest_ev.event_type if latest_ev else "none",
            "latest_event_time": (
                latest_ev.timestamp.strftime("%H:%M:%S") if latest_ev and latest_ev.timestamp else ""
            ),
        })

    # System-wide recent alerts ticker (last 20 flagged events)
    recent_alerts_raw = (
        EventLog.query.filter(
            (EventLog.is_flagged == True) | (EventLog.severity.in_(["warning", "critical"]))
        )
        .order_by(EventLog.timestamp.desc())
        .limit(20)
        .all()
    )

    alerts = []
    for a in recent_alerts_raw:
        cand_name = a.session.candidate.full_name if a.session and a.session.candidate else "Candidate"
        alerts.append({
            "id": a.id,
            "session_id": a.session_id,
            "candidate_name": cand_name,
            "event_type": a.event_type,
            "severity": a.severity,
            "details": a.details or "",
            "time": a.timestamp.strftime("%H:%M:%S") if a.timestamp else "",
        })

    return jsonify({
        "active_count": len(sessions_data),
        "sessions": sessions_data,
        "alerts": alerts,
        "timestamp": now.strftime("%H:%M:%S"),
    })


@admin_bp.route("/api/admin/terminate-session", methods=["POST"])
@admin_required
def api_terminate_session():
    """Remotely terminate an active student exam session from invigilator console."""
    from app.routes.exam import finalize_session

    data = request.get_json() or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    session = ExamSession.query.get_or_404(session_id)
    if session.status != "active":
        return jsonify({"error": "Session is not active", "status": session.status}), 400

    finalize_session(session, status="terminated")
    return jsonify({
        "success": True,
        "message": f"Session #{session.id} for {session.candidate.full_name} has been terminated.",
    })


@admin_bp.route("/admin/students")
@admin_required
def students():
    """Roster of registered candidates with webcam photos and ID documents."""
    candidates = (
        User.query.filter_by(role="candidate")
        .order_by(User.created_at.desc())
        .all()
    )
    return render_template("admin/students.html", candidates=candidates)


@admin_bp.route("/admin/students/<int:user_id>/verify", methods=["POST"])
@admin_required
def toggle_verify(user_id):
    """Approve or revoke student ID verification."""
    u = User.query.get_or_404(user_id)
    u.id_verified = not u.id_verified
    db.session.commit()
    status_str = "verified" if u.id_verified else "unverified"
    flash(f"Student {u.full_name} ID marked as {status_str}.", "success")
    return redirect(url_for("admin.students"))


@admin_bp.route("/admin/exams", methods=["GET", "POST"])
@admin_required
def manage_exams():
    """Catalog management: view and create exams."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        subject = request.form.get("subject", "General").strip()
        target_domain = request.form.get("target_domain", "All").strip()
        target_department = request.form.get("target_department", "All").strip()
        duration = int(request.form.get("duration_minutes", 60))
        questions = int(request.form.get("total_questions", 10))

        if not title:
            flash("Exam title is required.", "danger")
            return redirect(url_for("admin.manage_exams"))

        exam = AvailableExam(
            title=title,
            description=description,
            subject=subject,
            target_domain=target_domain or "All",
            target_department=target_department or "All",
            duration_minutes=duration,
            total_questions=questions,
            is_active=True,
        )
        db.session.add(exam)
        db.session.commit()
        flash(f"Exam '{title}' created successfully!", "success")
        return redirect(url_for("admin.manage_exams"))

    all_exams = AvailableExam.query.order_by(AvailableExam.id.desc()).all()
    return render_template("admin/exams.html", exams=all_exams)


@admin_bp.route("/admin/exams/<int:exam_id>/toggle", methods=["POST"])
@admin_required
def toggle_exam(exam_id):
    """Toggle exam availability (active / inactive)."""
    exam = AvailableExam.query.get_or_404(exam_id)
    exam.is_active = not exam.is_active
    db.session.commit()
    state = "active" if exam.is_active else "inactive"
    flash(f"Exam '{exam.title}' is now {state}.", "info")
    return redirect(url_for("admin.manage_exams"))


@admin_bp.route("/admin/analytics")
@admin_required
def analytics():
    """Native analytics dashboard – full Streamlit feature set inside Flask (no Streamlit required)."""
    from app.services.analytics_data import (
        load_analytics_overview,
        load_all_students_data,
        load_scores_data,
        load_events_data,
        load_clustering_data,
        load_risk_data,
        load_drilldown_data,
        load_exports_meta,
    )

    page = (request.args.get("page") or "overview").strip().lower()
    allowed = {
        "overview",
        "students",
        "scores",
        "events",
        "clustering",
        "risk",
        "drilldown",
        "exports",
    }
    if page not in allowed:
        page = "overview"

    # Base overview always available for KPIs / sidebar
    overview = load_analytics_overview()
    ctx = {
        "page": page,
        "total_attempts": overview["total_attempts"],
        "unique_students": overview["unique_students"],
        "scored_sessions": overview["scored_sessions"],
        "avg_integrity": overview["avg_integrity"],
        "high_risk_count": overview["high_risk_count"],
        "risk_distribution": overview["risk_distribution"],
        "avg_by_category": overview["avg_by_category"],
        "latest_attempts": overview["latest_attempts"],
        # Defaults so Jinja |tojson never sees missing vars on other pages
        "hist_labels": [],
        "hist_counts": [],
        "scatter": [],
        "box_by_risk": {},
        "scored": [],
        "avg_score": 0,
        "event_type_labels": [],
        "event_type_values": [],
        "flagged_count": 0,
        "total_events": 0,
        "recent_events": [],
        "points": [],
        "summary": [],
        "cluster_labels": {},
        "ok": False,
        "k": 3,
        "message": None,
        "risk_labels": [],
        "risk_counts": [],
        "risk_colors": [],
        "high_risk_sessions": [],
        "session_ids": [],
        "selected": None,
        "selected_id": None,
        "ai_summary": None,
        "model_used": None,
        "events": [],
        "files": {},
        "student_summary": [],
        "all_attempts": [],
        "total_sessions": 0,
    }

    if page == "students":
        ctx.update(load_all_students_data())
    elif page == "scores":
        ctx.update(load_scores_data())
    elif page == "events":
        ctx.update(load_events_data())
    elif page == "clustering":
        try:
            k = int(request.args.get("k", 3))
        except (TypeError, ValueError):
            k = 3
        ctx.update(load_clustering_data(k=k))
    elif page == "risk":
        ctx.update(load_risk_data())
    elif page == "drilldown":
        sid = request.args.get("session_id", type=int)
        ctx.update(load_drilldown_data(session_id=sid))
    elif page == "exports":
        ctx.update(load_exports_meta())

    return render_template("admin/analytics.html", **ctx)


@admin_bp.route("/admin/analytics/refresh-exports", methods=["POST"])
@admin_required
def refresh_exports():
    """Regenerate CSV/JSON exports from live SQLite (same as Streamlit refresh)."""
    try:
        result = export_analytics_data()
        # Also write cluster assignments if possible
        try:
            from app.services.analytics_data import load_clustering_data
            import pandas as pd
            from pathlib import Path
            from flask import current_app

            cluster = load_clustering_data(k=3)
            if cluster.get("ok") and cluster.get("points"):
                root = Path(current_app.root_path).parent
                out = root / "data" / "exports" / "cluster_assignments.csv"
                pd.DataFrame(cluster["points"]).to_csv(out, index=False)
        except Exception:
            pass
        flash(
            f"Exports refreshed: {result.get('sessions', 0)} sessions, "
            f"{result.get('events', 0)} events, {result.get('reports', 0)} AI reports.",
            "success",
        )
    except Exception as e:
        flash(f"Export failed: {e}", "danger")
    return redirect(url_for("admin.analytics", page="exports"))


@admin_bp.route("/admin/analytics/download/<path:filename>")
@admin_required
def download_export(filename):
    """Download an analytics export file."""
    from flask import send_from_directory, current_app
    from pathlib import Path

    allowed = {
        "integrity_scores.csv",
        "session_logs.csv",
        "ai_reports.json",
        "cluster_assignments.csv",
    }
    if filename not in allowed:
        flash("Unknown export file.", "danger")
        return redirect(url_for("admin.analytics", page="exports"))

    root = Path(current_app.root_path).parent
    export_dir = root / "data" / "exports"
    path = export_dir / filename
    if not path.exists():
        # Generate on the fly
        try:
            export_analytics_data()
        except Exception:
            pass
    if not path.exists():
        flash(f"{filename} not found. Click Refresh exports first.", "warning")
        return redirect(url_for("admin.analytics", page="exports"))
    return send_from_directory(str(export_dir), filename, as_attachment=True)
