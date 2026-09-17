"""Synthetic session data generator (Faker)."""
import os, sys, random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from faker import Faker
from app import create_app, db
from app.models.models import User, ExamSession, EventLog, IntegrityScore, AIReport, AvailableExam
from app.services.scoring import compute_integrity_score
from app.services.ai_agent import generate_integrity_report

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_CANDIDATES = 35
NUM_INVIGILATORS = 2


def main():
    app = create_app()
    with app.app_context():
        # Invigilators
        for i in range(NUM_INVIGILATORS):
            email = f"invigilator{i+1}@examguard.edu"
            if not User.query.filter_by(email=email).first():
                u = User(email=email, full_name=fake.name(), role="invigilator",
                         id_verified=True, id_type="college_id", id_number=f"INV-{i+1:03d}",
                         academic_status="Faculty / Invigilator",
                         college="University Examination Cell",
                         domain="Faculty of Engineering",
                         department="Computer Science & Engineering",
                         year_of_study="Faculty Staff")
                u.set_password("invigilator123")
                db.session.add(u)

        # Candidates
        for i in range(NUM_CANDIDATES):
            email = f"candidate{i+1:03d}@student.edu"
            if User.query.filter_by(email=email).first():
                continue
            u = User(
                email=email, full_name=fake.name(), role="candidate",
                id_verified=True,
                id_type=random.choice(["aadhaar", "college_id", "passport"]),
                id_number=fake.bothify(text="????-####-####"),
                academic_status=random.choice(["Currently Studying", "Graduated"]),
                college=fake.company() + " University",
                domain=random.choice(["B.Tech", "MCA", "BA"]),
                department=random.choice(["Computer Science & Engineering (CSE)", "Computer Applications", "Economics"]),
                year_of_study=random.choice(["1st Year", "2nd Year", "3rd Year", "4th Year"]),
            )
            u.set_password("candidate123")
            db.session.add(u)
        db.session.commit()
        
        # Seed exam catalog
        if AvailableExam.query.count() == 0:
            for item in [
                {"title": "Data Structures Midterm", "description": "Arrays, lists, trees.", "duration_minutes": 60, "total_questions": 20, "subject": "Computer Science"},
                {"title": "Python Programming Assessment", "description": "Core Python & OOP.", "duration_minutes": 45, "total_questions": 15, "subject": "Programming"},
                {"title": "Database Systems Quiz", "description": "SQL and normalization.", "duration_minutes": 40, "total_questions": 12, "subject": "Database"},
                {"title": "Computer Networks Final", "description": "OSI, TCP/IP, routing.", "duration_minutes": 90, "total_questions": 25, "subject": "Networks"},
                {"title": "Machine Learning Basics", "description": "Supervised learning intro.", "duration_minutes": 60, "total_questions": 18, "subject": "AI / ML"},
            ]:
                db.session.add(AvailableExam(**item, is_active=True))
            db.session.commit()
            print("Exam catalog seeded.")

        print("Users ready.")

        profiles = ["low"] * 18 + ["medium"] * 12 + ["high"] * 5
        random.shuffle(profiles)
        candidates = User.query.filter_by(role="candidate").all()

        for idx, cand in enumerate(candidates):
            for _ in range(random.randint(1, 2)):
                risk = profiles[idx % len(profiles)]
                start = fake.date_time_between(start_date="-20d", end_date="-1d")
                duration = random.choice([45, 60, 90])
                end = start + timedelta(minutes=duration)
                session = ExamSession(
                    candidate_id=cand.id,
                    exam_title=random.choice([
                        "Data Structures Midterm", "Python Assessment",
                        "DBMS Quiz", "Networks Final", "ML Basics Test",
                    ]),
                    status="submitted", started_at=start, ended_at=end,
                    duration_minutes=duration,
                )
                db.session.add(session)
                db.session.flush()

                # Events by risk
                if risk == "low":
                    n_tabs, n_focus, n_absent, absent_dur, n_multi, n_audio = (
                        random.randint(0, 2), random.randint(0, 2), random.randint(0, 1),
                        random.randint(5, 50), 0, random.randint(0, 1))
                elif risk == "medium":
                    n_tabs, n_focus, n_absent, absent_dur, n_multi, n_audio = (
                        random.randint(3, 6), random.randint(3, 7), random.randint(1, 3),
                        random.randint(60, 150), random.randint(0, 1), random.randint(1, 3))
                else:
                    n_tabs, n_focus, n_absent, absent_dur, n_multi, n_audio = (
                        random.randint(7, 14), random.randint(6, 15), random.randint(3, 5),
                        random.randint(180, 500), random.randint(1, 3), random.randint(3, 7))

                events = []
                def add(etype, dur=0, flagged=False, sev="info"):
                    ts = start + timedelta(seconds=random.randint(20, duration * 60 - 20))
                    events.append(EventLog(
                        session_id=session.id, event_type=etype, severity=sev,
                        timestamp=ts, duration_seconds=dur, is_flagged=flagged,
                        details=etype,
                    ))

                for _ in range(n_tabs):
                    add("tab_switch", flagged=n_tabs > 3, sev="warning" if n_tabs > 3 else "info")
                for _ in range(n_focus):
                    add("focus_loss", random.randint(3, 30), n_focus > 5, "warning" if n_focus > 5 else "info")
                rem = absent_dur
                for i in range(max(1, n_absent)):
                    d = rem // max(1, n_absent - i)
                    rem -= d
                    add("face_absent", d, True, "critical" if d > 120 else "warning")
                for _ in range(n_multi):
                    add("multi_face", 0, True, "critical")
                for _ in range(n_audio):
                    add("audio_spike", 0, n_audio > 4, "warning" if n_audio > 4 else "info")

                for e in events:
                    db.session.add(e)
                db.session.flush()

                result = compute_integrity_score(
                    [{"event_type": e.event_type, "duration_seconds": e.duration_seconds or 0} for e in events],
                    duration * 60,
                )
                db.session.add(IntegrityScore(
                    session_id=session.id, score=result["score"], risk_label=result["risk_label"],
                    tab_switch_count=result["tab_switch_count"], focus_loss_count=result["focus_loss_count"],
                    face_absent_seconds=result["face_absent_seconds"], multi_face_count=result["multi_face_count"],
                    audio_spike_count=result.get("audio_spike_count", 0),
                    face_presence_ratio=result["face_presence_ratio"],
                ))
                ai = generate_integrity_report({"candidate_name": cand.full_name, **result})
                db.session.add(AIReport(session_id=session.id, summary_text=ai["summary_text"], model_used=ai["model_used"]))

        db.session.commit()
        print("Sessions + scores + AI reports created.")

        # Exports
        import pandas as pd, json
        export = ROOT / "data" / "exports"
        export.mkdir(parents=True, exist_ok=True)
        rows = []
        for s in ExamSession.query.all():
            sc = s.integrity_score
            rows.append({
                "session_id": s.id, "candidate_id": s.candidate_id,
                "candidate_name": s.candidate.full_name if s.candidate else "",
                "exam_title": s.exam_title, "status": s.status,
                "started_at": s.started_at, "ended_at": s.ended_at,
                "duration_minutes": s.duration_minutes,
                "score": sc.score if sc else None, "risk_label": sc.risk_label if sc else None,
                "tab_switch_count": sc.tab_switch_count if sc else 0,
                "focus_loss_count": sc.focus_loss_count if sc else 0,
                "face_absent_seconds": sc.face_absent_seconds if sc else 0,
                "multi_face_count": sc.multi_face_count if sc else 0,
                "audio_spike_count": sc.audio_spike_count if sc else 0,
                "face_presence_ratio": sc.face_presence_ratio if sc else 1.0,
            })
        pd.DataFrame(rows).to_csv(export / "integrity_scores.csv", index=False)
        ev = [{"event_id": e.id, "session_id": e.session_id, "event_type": e.event_type,
               "severity": e.severity, "timestamp": e.timestamp, "duration_seconds": e.duration_seconds,
               "is_flagged": e.is_flagged} for e in EventLog.query.all()]
        pd.DataFrame(ev).to_csv(export / "session_logs.csv", index=False)
        reports = [{"session_id": r.session_id, "summary_text": r.summary_text,
                    "model_used": r.model_used,
                    "generated_at": r.generated_at.isoformat() if r.generated_at else None}
                   for r in AIReport.query.all()]
        with open(export / "ai_reports.json", "w") as f:
            json.dump(reports, f, indent=2)
        print(f"Exports → data/exports/ ({len(rows)} sessions)")


if __name__ == "__main__":
    main()
