"""Test assignment marks calculation, submission, and display for student and invigilator."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app, db
from app.models.models import User, AvailableExam, ExamSession

def test_submission_and_scores():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with app.app_context():
        candidate = User.query.filter_by(role="candidate").first()
        invigilator = User.query.filter(User.role.in_(["invigilator", "admin"])).first()
        exam = AvailableExam.query.filter(AvailableExam.title.like("CSE-101%")).first()

        # 1. Create an active session
        session = ExamSession(
            candidate_id=candidate.id,
            exam_id=exam.id,
            exam_title=exam.title,
            status="active",
            duration_minutes=exam.duration_minutes,
        )
        db.session.add(session)
        db.session.commit()
        sess_id = session.id
        print(f"[OK] Created test session #{sess_id}")

        # 2. Candidate submits answers:
        # CSE-101 answers in catalog: q1:b, q2:b, q3:a, q4:b, q5:a
        # Candidate answers 4 correct (q1:b, q2:b, q3:a, q4:b) and 1 wrong (q5:c) -> 4/5 (80.0%)
        candidate.set_password("Pass123!")
        db.session.commit()

        client.post("/login", data={"email": candidate.email, "password": "Pass123!"}, follow_redirects=True)

        submit_data = {
            "q1": "b",
            "q2": "b",
            "q3": "a",
            "q4": "b",
            "q5": "c",  # wrong
        }
        resp = client.post(f"/session/{sess_id}/submit", data=submit_data, follow_redirects=True)
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)

        # 3. Verify Candidate sees Assignment Marks on report page
        assert "Assignment Marks" in html
        assert "4/5" in html
        assert "80.0%" in html
        assert "PASSED" in html
        assert "Question" in html
        assert "Student Answer" in html
        assert "Correct Answer" in html
        assert "Integrity Score" in html
        print("[OK] Candidate sees Assignment Marks (4/5 80.0% PASSED) and Question Breakdown on report page.")

        # 4. Verify Student Dashboard shows the new Assignment Score in history
        dash_resp = client.get("/student")
        assert dash_resp.status_code == 200
        dash_html = dash_resp.get_data(as_text=True)
        assert "4/5 (80.0%)" in dash_html
        print("[OK] Candidate Dashboard displays Assignment Score in exam history table.")

        # 5. Verify Invigilator can view the report and see the Assignment Marks
        client.get("/logout")
        invigilator.set_password("AdminPass123!")
        db.session.commit()

        client.post("/login", data={"email": invigilator.email, "password": "AdminPass123!"}, follow_redirects=True)

        invig_report_resp = client.get(f"/session/{sess_id}/report")
        assert invig_report_resp.status_code == 200
        invig_html = invig_report_resp.get_data(as_text=True)
        assert "Assignment Marks" in invig_html
        assert "4/5" in invig_html
        assert "80.0%" in invig_html
        assert "Question" in invig_html
        assert "Student Answer" in invig_html
        assert "Correct Answer" in invig_html
        assert "Return to Invigilator Console" in invig_html
        print("[OK] Invigilator accesses session report and views both Assignment Marks and Integrity Telemetry.")

        # 6. Verify Invigilator Dashboard shows the Assignment Marks in Sessions Log table
        admin_dash_resp = client.get("/admin")
        assert admin_dash_resp.status_code == 200
        admin_dash_html = admin_dash_resp.get_data(as_text=True)
        assert "4/5 (80.0%)" in admin_dash_html
        print("[OK] Invigilator Console displays Assignment Score in Recent Sessions table.")

        # Clean up test session
        s_to_del = ExamSession.query.get(sess_id)
        if s_to_del:
            db.session.delete(s_to_del)
            db.session.commit()
        print(f"[OK] Cleaned up test session #{sess_id}")
        print("\n=== ALL ASSIGNMENT MARKS TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_submission_and_scores()
