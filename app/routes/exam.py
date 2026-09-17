"""Examination session management + test catalog."""
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, jsonify
)
from flask_login import login_required, current_user
from app import db
from app.models.models import (
    ExamSession, EventLog, IntegrityScore, AIReport, AvailableExam
)
from app.services.scoring import compute_integrity_score, MAX_VIOLATIONS
from app.services.ai_agent import generate_integrity_report
from app.services.export_data import export_analytics_data
from app.services.exam_catalog import (
    DOMAIN_CATALOG,
    seed_domain_catalog,
    get_exam_questions,
    grade_exam,
)

exam_bp = Blueprint("exam", __name__)


def ensure_exam_catalog():
    """Ensure all 25 domain assessments (5 domains x 5 tests) are seeded."""
    seed_domain_catalog()


def finalize_session(session, status="submitted"):
    """Compute score + AI report and set final status."""
    session.status = status
    if not session.ended_at:
        session.ended_at = datetime.utcnow()
    db.session.commit()

    # Avoid duplicate scores
    if session.integrity_score:
        return

    events = [
        {
            "event_type": e.event_type,
            "duration_seconds": e.duration_seconds or 0,
            "is_flagged": e.is_flagged,
        }
        for e in session.events
    ]
    duration_sec = session.duration_minutes * 60
    if session.started_at and session.ended_at:
        duration_sec = max(1, int((session.ended_at - session.started_at).total_seconds()))

    result = compute_integrity_score(events, duration_sec)
    score = IntegrityScore(
        session_id=session.id,
        score=result["score"],
        risk_label=result["risk_label"],
        tab_switch_count=result["tab_switch_count"],
        focus_loss_count=result["focus_loss_count"],
        face_absent_seconds=result["face_absent_seconds"],
        multi_face_count=result["multi_face_count"],
        audio_spike_count=result.get("audio_spike_count", 0),
        face_presence_ratio=result["face_presence_ratio"],
    )
    db.session.add(score)

    candidate_name = session.candidate.full_name if session.candidate else "Candidate"
    ai = generate_integrity_report({"candidate_name": candidate_name, **result})
    if status == "terminated":
        ai["summary_text"] = (
            f"Session was auto-terminated after exceeding {MAX_VIOLATIONS} rule violations. "
            + ai["summary_text"]
        )
    if session.test_score:
        ai["summary_text"] += f" Assessment score achieved: {session.test_score}."

    db.session.add(AIReport(
        session_id=session.id,
        summary_text=ai["summary_text"],
        model_used=ai["model_used"],
    ))
    db.session.commit()
    try:
        export_analytics_data()
    except Exception:
        pass  # never block submit if export fails


_finalize_session = finalize_session


@exam_bp.route("/student")
@exam_bp.route("/home")
@login_required
def candidate_home():
    if current_user.role != "candidate":
        return redirect(url_for("admin.dashboard"))
    if not current_user.is_profile_complete:
        return redirect(url_for("auth.verify_id"))

    ensure_exam_catalog()
    raw_exams = AvailableExam.query.filter_by(is_active=True).order_by(AvailableExam.subject, AvailableExam.title).all()

    exams_with_eligibility = []
    eligible_count = 0
    for ex in raw_exams:
        is_el, reason = ex.is_eligible(current_user)
        if is_el:
            eligible_count += 1
        exams_with_eligibility.append({
            "exam": ex,
            "is_eligible": is_el,
            "eligibility_reason": reason,
        })

    sessions = (
        ExamSession.query.filter_by(candidate_id=current_user.id)
        .order_by(ExamSession.created_at.desc())
        .all()
    )
    return render_template(
        "candidate_home.html",
        exams_with_eligibility=exams_with_eligibility,
        eligible_count=eligible_count,
        exams=raw_exams,
        sessions=sessions,
        domain_catalog=DOMAIN_CATALOG,
    )



@exam_bp.route("/progress")
@exam_bp.route("/student/progress")
@login_required
def progress():
    """Student performance & proctoring analytics dashboard (native Flask)."""
    if current_user.role != "candidate":
        flash("Student progress dashboard is reserved for candidates.", "warning")
        return redirect(url_for("admin.dashboard"))

    from app.services.analytics_data import _category_from_exam, _difficulty_from_exam, _safe_float

    sel_category = request.args.get("category", "All Categories").strip()
    sel_difficulty = request.args.get("difficulty", "All Levels").strip()

    sessions = (
        ExamSession.query.filter(
            ExamSession.candidate_id == current_user.id,
            ExamSession.status.in_(["submitted", "terminated"]),
        )
        .order_by(ExamSession.created_at.asc())
        .all()
    )

    # Attach derived category / difficulty / scores for filtering
    rows = []
    categories = set()
    difficulties = set()
    for s in sessions:
        exam = s.exam
        subject = exam.subject if exam else None
        cat = _category_from_exam(s.exam_title or "", subject)
        diff = _difficulty_from_exam(
            s.exam_title or "",
            exam.duration_minutes if exam else s.duration_minutes,
            exam.total_questions if exam else None,
        )
        categories.add(cat)
        difficulties.add(diff)
        test_sc = _safe_float(s.test_score)
        # test_score sometimes stored as "7/10 (70%)"
        if test_sc is None and s.test_score:
            try:
                import re
                m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*%", str(s.test_score))
                if m:
                    test_sc = float(m.group(1))
                else:
                    m2 = re.search(r"([0-9]+)\s*/\s*([0-9]+)", str(s.test_score))
                    if m2:
                        test_sc = round(100.0 * int(m2.group(1)) / max(1, int(m2.group(2))), 1)
            except Exception:
                pass
        integrity = s.integrity_score.score if s.integrity_score else None
        risk = s.integrity_score.risk_label if s.integrity_score else None
        correct_n, total_n = None, None
        if s.test_score:
            try:
                import re
                m2 = re.search(r"([0-9]+)\s*/\s*([0-9]+)", str(s.test_score))
                if m2:
                    correct_n = int(m2.group(1))
                    total_n = int(m2.group(2))
            except Exception:
                pass
        if correct_n is None and test_sc is not None and exam:
            total_n = exam.total_questions or 5
            correct_n = int(round((test_sc / 100.0) * total_n))
        rows.append({
            "session": s,
            "category": cat,
            "difficulty": diff,
            "test_score": test_sc,
            "integrity": integrity,
            "risk": risk,
            "correct": correct_n,
            "total_q": total_n,
        })

    if sel_category and sel_category != "All Categories":
        rows = [r for r in rows if r["category"] == sel_category]
    if sel_difficulty and sel_difficulty != "All Levels":
        rows = [r for r in rows if r["difficulty"] == sel_difficulty]

    exams_attempted = len(rows)
    test_scores = [r["test_score"] for r in rows if r["test_score"] is not None]
    has_results = len(test_scores) > 0
    avg_test_score = round(sum(test_scores) / len(test_scores), 1) if test_scores else 0.0
    best_score = round(max(test_scores), 1) if test_scores else 0.0
    latest_score = round(test_scores[-1], 1) if test_scores else 0.0

    integrity_scores = [r["integrity"] for r in rows if r["integrity"] is not None]
    avg_integrity_score = round(sum(integrity_scores) / len(integrity_scores), 1) if integrity_scores else 0.0
    high_risk_count = sum(1 for r in rows if r["risk"] == "High")

    # Answer breakdown from scored sessions (correct vs wrong)
    total_correct = 0
    total_incorrect = 0
    total_unanswered = 0
    for r in rows:
        if r.get("correct") is not None and r.get("total_q"):
            c = max(0, int(r["correct"]))
            tot = max(c, int(r["total_q"]))
            total_correct += c
            total_incorrect += max(0, tot - c)
        elif r.get("test_score") is not None:
            # Fallback: treat each exam as 5 questions
            tot = 5
            c = int(round((r["test_score"] / 100.0) * tot))
            total_correct += c
            total_incorrect += max(0, tot - c)

    risk_counts = {
        "Low": sum(1 for r in rows if r["risk"] == "Low"),
        "Medium": sum(1 for r in rows if r["risk"] == "Medium"),
        "High": sum(1 for r in rows if r["risk"] == "High"),
    }

    timeline_labels = [
        (r["session"].created_at.strftime("%b %d") if r["session"].created_at else f"#{r['session'].id}")
        for r in rows
    ]
    timeline_test_scores = [r["test_score"] for r in rows]
    timeline_integrity_scores = [r["integrity"] for r in rows]

    category_map = {}
    for r in rows:
        category_map.setdefault(r["category"], [])
        if r["test_score"] is not None:
            category_map[r["category"]].append(r["test_score"])
    category_stats = {}
    for cat_name, scores_arr in category_map.items():
        if scores_arr:
            category_stats[cat_name] = {
                "attempts": len(scores_arr),
                "avg_score": round(sum(scores_arr) / len(scores_arr), 1),
                "best_score": round(max(scores_arr), 1),
            }

    diff_map = {}
    for r in rows:
        diff_map.setdefault(r["difficulty"], [])
        if r["test_score"] is not None:
            diff_map[r["difficulty"]].append(r["test_score"])
    difficulty_stats = {}
    for diff_name, scores_arr in diff_map.items():
        if scores_arr:
            difficulty_stats[diff_name] = {
                "attempts": len(scores_arr),
                "avg_score": round(sum(scores_arr) / len(scores_arr), 1),
                "best_score": round(max(scores_arr), 1),
            }

    personalized_tips = []
    if has_results:
        if avg_test_score < 70:
            personalized_tips.append(
                "Focus on reviewing incorrect answers and revisit fundamental concepts before attempting another test."
            )
        elif avg_test_score >= 85:
            personalized_tips.append(
                "Excellent academic performance overall! Maintain your consistent study routine."
            )
        for cat_n, c_stat in category_stats.items():
            if c_stat["avg_score"] < 70:
                personalized_tips.append(
                    f"Your average score in {cat_n} is {c_stat['avg_score']}%. Practice more questions in this category."
                )
        if avg_integrity_score < 80 or high_risk_count > 0:
            personalized_tips.append(
                "Review exam environment requirements and keep camera, focus, and microphone stable during assessments."
            )
    if not personalized_tips:
        personalized_tips.append(
            "Keep up the great work! Complete more assessments across different categories for deeper insights."
        )

    return render_template(
        "progress.html",
        exams_attempted=exams_attempted,
        has_results=has_results,
        avg_test_score=avg_test_score,
        best_score=best_score,
        latest_score=latest_score,
        avg_integrity_score=avg_integrity_score,
        high_risk_count=high_risk_count,
        total_correct=total_correct,
        total_incorrect=total_incorrect,
        total_unanswered=total_unanswered,
        risk_counts=risk_counts,
        timeline_labels=timeline_labels,
        timeline_test_scores=timeline_test_scores,
        timeline_integrity_scores=timeline_integrity_scores,
        category_stats=category_stats,
        difficulty_stats=difficulty_stats,
        personalized_tips=personalized_tips,
        categories=sorted(categories),
        difficulties=sorted(difficulties),
        selected_category=sel_category,
        selected_difficulty=sel_difficulty,
    )



def invigilator_home():
    """Legacy redirect to admin console."""
    return redirect(url_for("admin.dashboard"))



@exam_bp.route("/exam/<int:exam_id>/precheck")
@login_required
def precheck(exam_id):
    """System check + face match + rules acceptance before start."""
    if not current_user.is_profile_complete:
        flash("Complete ID verification first.", "warning")
        return redirect(url_for("auth.verify_id"))
    if not current_user.photo_path:
        flash("Registration face photo is required. Please re-register with a webcam photo.", "danger")
        return redirect(url_for("exam.candidate_home"))
    ensure_exam_catalog()
    exam = AvailableExam.query.get_or_404(exam_id)
    if not exam.is_active:
        flash("This test is not available.", "warning")
        return redirect(url_for("exam.candidate_home"))

    # Eligibility check
    is_el, reason = exam.is_eligible(current_user)
    if not is_el:
        flash(f"Cannot take this exam: {reason}", "danger")
        return redirect(url_for("exam.candidate_home"))

    return render_template("precheck.html", exam=exam, max_violations=MAX_VIOLATIONS)


@exam_bp.route("/exam/<int:exam_id>/start", methods=["POST"])
@login_required
def start_session(exam_id):
    """Create session only after media ready, face match, and rules accepted."""
    if not current_user.is_profile_complete:
        flash("Complete ID verification first.", "warning")
        return redirect(url_for("auth.verify_id"))

    exam = AvailableExam.query.get_or_404(exam_id)

    # Server-side eligibility enforcement
    is_el, reason = exam.is_eligible(current_user)
    if not is_el:
        flash(f"Exam enrollment restricted: {reason}", "danger")
        return redirect(url_for("exam.candidate_home"))

    media_ok = request.form.get("media_ready") == "1"
    face_ok = request.form.get("face_verified") == "1"
    rules_ok = request.form.get("rules_accepted") == "1"

    if not rules_ok:
        flash("You must accept the exam rules and conditions before starting.", "danger")
        return redirect(url_for("exam.precheck", exam_id=exam_id))
    if not media_ok:
        flash("Camera and microphone must be enabled before starting.", "danger")
        return redirect(url_for("exam.precheck", exam_id=exam_id))
    if not face_ok:
        flash("Face must match your registration photo before starting the exam.", "danger")
        return redirect(url_for("exam.precheck", exam_id=exam_id))

    session = ExamSession(
        candidate_id=current_user.id,
        exam_id=exam.id,
        exam_title=exam.title,
        status="active",
        started_at=datetime.utcnow(),
        duration_minutes=exam.duration_minutes,
    )
    db.session.add(session)
    db.session.commit()
    return redirect(url_for("exam.take_exam", session_id=session.id))


@exam_bp.route("/session/<int:session_id>")
@login_required
def take_exam(session_id):
    session = ExamSession.query.get_or_404(session_id)
    if session.candidate_id != current_user.id and current_user.role not in ("invigilator", "admin"):
        flash("Access denied.", "danger")
        return redirect(url_for("exam.candidate_home"))
    if session.status == "terminated":
        # finalize report if needed
        if not session.integrity_score:
            _finalize_session(session, "terminated")
        flash("This assessment was closed due to repeated rule violations.", "danger")
        return redirect(url_for("exam.session_report", session_id=session.id))
    if session.status != "active" and current_user.role == "candidate":
        return redirect(url_for("exam.session_report", session_id=session.id))

    exam_title = session.exam_title or (session.exam.title if session.exam else "General")
    questions = get_exam_questions(exam_title)

    return render_template(
        "exam_session.html",
        session=session,
        questions=questions,
        max_violations=MAX_VIOLATIONS,
    )


@exam_bp.route("/session/<int:session_id>/submit", methods=["POST"])
@login_required
def submit_session(session_id):
    session = ExamSession.query.get_or_404(session_id)
    if session.candidate_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    status = "submitted"
    if request.form.get("terminated") == "1" or session.status == "terminated":
        status = "terminated"

    # Evaluate candidate answers
    exam_title = session.exam_title or (session.exam.title if session.exam else "")
    grade_result = grade_exam(exam_title, request.form)
    session.test_score = grade_result["score_str"]

    import json
    score_event = EventLog(
        session_id=session.id,
        event_type="test_submission",
        severity="info",
        details=json.dumps({
            "score": grade_result["score"],
            "total": grade_result["total"],
            "percentage": grade_result["percentage"],
            "score_str": grade_result["score_str"],
            "passed": grade_result["passed"],
            "results": grade_result["results"],
        }),
        is_flagged=False,
    )
    db.session.add(score_event)
    db.session.commit()

    _finalize_session(session, status)
    if status == "terminated":
        flash(f"Assessment closed due to rule violations. Assignment Score: {grade_result['score_str']}", "danger")
    else:
        flash(f"Assessment submitted successfully! Assignment Score: {grade_result['score_str']}", "success")
    return redirect(url_for("exam.session_report", session_id=session.id))


@exam_bp.route("/session/<int:session_id>/report")
@login_required
def session_report(session_id):
    import json
    session = ExamSession.query.get_or_404(session_id)
    if session.candidate_id != current_user.id and current_user.role not in ("invigilator", "admin"):
        flash("Access denied.", "danger")
        return redirect(url_for("exam.candidate_home"))
    if session.status == "terminated" and not session.integrity_score:
        _finalize_session(session, "terminated")

    # Retrieve graded assignment details
    grade_details = None
    test_sub_ev = EventLog.query.filter_by(session_id=session.id, event_type="test_submission").first()
    if test_sub_ev and test_sub_ev.details:
        try:
            grade_details = json.loads(test_sub_ev.details)
        except Exception:
            pass

    # Fallback to parsing session.test_score if JSON details not in event log
    if not grade_details and session.test_score:
        try:
            parts = session.test_score.split()
            score_part = parts[0]
            pct_part = parts[1].strip("()%") if len(parts) > 1 else "0"
            scored, total = score_part.split("/")
            grade_details = {
                "score": int(scored),
                "total": int(total),
                "percentage": float(pct_part),
                "score_str": session.test_score,
                "passed": float(pct_part) >= 40.0,
                "results": [],
            }
        except Exception:
            pass

    return render_template(
        "session_report.html",
        session=session,
        grade_details=grade_details,
    )
