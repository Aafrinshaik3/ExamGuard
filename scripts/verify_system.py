"""Comprehensive automated system verification script."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app, db
from app.models.models import User, AvailableExam, ExamSession
from app.services.exam_catalog import seed_domain_catalog

def run_tests():
    app = create_app()
    with app.app_context():
        print("=== 1. VERIFYING SEEDING & CATALOG ===")
        seed_domain_catalog()
        total_exams = AvailableExam.query.count()
        print(f"Total Available Exams: {total_exams}")
        assert total_exams >= 35, f"Expected at least 35 exams, got {total_exams}"

        distinct_domains = [r[0] for r in AvailableExam.query.with_entities(AvailableExam.target_domain).distinct().all()]
        print(f"Target Domains in Catalog: {distinct_domains}")
        assert "B.Tech" in distinct_domains
        assert "MCA" in distinct_domains
        assert "BA" in distinct_domains
        assert "All" in distinct_domains

        print("=== 2. VERIFYING DEMO REMOVAL ===")
        demo_candidates = User.query.filter(User.email.like("candidate%@student.edu")).all()
        demo_invigilators = User.query.filter(User.email.like("invigilator%@examguard.edu")).all()
        print(f"Demo Candidates remaining: {len(demo_candidates)}")
        print(f"Demo Invigilators remaining: {len(demo_invigilators)}")
        assert len(demo_candidates) == 0, "Demo candidates still exist!"
        assert len(demo_invigilators) == 0, "Demo invigilators still exist!"

        print("=== 3. VERIFYING GENUINE USERS & PROFILES ===")
        users = User.query.all()
        print(f"Total Users in DB: {len(users)}")
        for u in users:
            print(f"User: {u.email} | Role: {u.role} | Status: {u.academic_status} | College: {u.college} | Domain: {u.domain} | Dept: {u.department} | Year: {u.year_of_study}")
            assert hasattr(u, "academic_status")
            assert hasattr(u, "college")
            assert hasattr(u, "domain")
            assert hasattr(u, "department")
            assert hasattr(u, "year_of_study")

        print("=== 4. VERIFYING ELIGIBILITY ENGINE ===")
        # Test Mock B.Tech CSE Student
        class MockUser:
            def __init__(self, role, status, domain, dept, year):
                self.is_authenticated = True
                self.role = role
                self.academic_status = status
                self.domain = domain
                self.department = dept
                self.year_of_study = year

        btech_user = MockUser("candidate", "Currently Studying", "B.Tech", "Computer Science & Engineering (CSE)", "3rd Year")
        mca_user = MockUser("candidate", "Currently Studying", "MCA", "Computer Applications", "2nd Year")
        ba_user = MockUser("candidate", "Currently Studying", "BA", "Economics", "2nd Year")
        beginner_user = MockUser("candidate", "Beginner", "Other", "General", "Beginner / Self-Learner")

        cse_exam = AvailableExam.query.filter(AvailableExam.title.like("CSE-101%")).first()
        mca_exam = AvailableExam.query.filter(AvailableExam.title.like("MCA-101%")).first()
        ba_exam = AvailableExam.query.filter(AvailableExam.title.like("BA-102%")).first()
        gen_exam = AvailableExam.query.filter(AvailableExam.title.like("GEN-101%")).first()

        assert cse_exam is not None, "CSE-101 not found"
        assert mca_exam is not None, "MCA-101 not found"
        assert ba_exam is not None, "BA-102 not found"
        assert gen_exam is not None, "GEN-101 not found"

        # B.Tech student checks
        ok, msg = cse_exam.is_eligible(btech_user)
        print(f"B.Tech CSE student taking CSE-101: {ok} ({msg})")
        assert ok is True

        ok, msg = mca_exam.is_eligible(btech_user)
        print(f"B.Tech CSE student taking MCA-101: {ok} ({msg})")
        assert ok is False

        ok, msg = gen_exam.is_eligible(btech_user)
        print(f"B.Tech CSE student taking GEN-101: {ok} ({msg})")
        assert ok is True

        # MCA student checks
        ok, msg = mca_exam.is_eligible(mca_user)
        print(f"MCA student taking MCA-101: {ok} ({msg})")
        assert ok is True

        ok, msg = cse_exam.is_eligible(mca_user)
        print(f"MCA student taking CSE-101: {ok} ({msg})")
        assert ok is False

        # BA student checks
        ok, msg = ba_exam.is_eligible(ba_user)
        print(f"BA student taking BA-102: {ok} ({msg})")
        assert ok is True

        ok, msg = cse_exam.is_eligible(ba_user)
        print(f"BA student taking CSE-101: {ok} ({msg})")
        assert ok is False

        # Beginner student checks
        ok, msg = gen_exam.is_eligible(beginner_user)
        print(f"Beginner taking GEN-101: {ok} ({msg})")
        assert ok is True

        ok, msg = cse_exam.is_eligible(beginner_user)
        print(f"Beginner taking CSE-101: {ok} ({msg})")
        assert ok is False

        print("\nAll eligibility checks passed successfully!")
        print("=== 5. SIMULATING NEW STUDENT REGISTRATION ===")
        test_email = "newstudent_test@college.edu"
        existing = User.query.filter_by(email=test_email).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        new_student = User(
            email=test_email,
            full_name="Alex Mercer",
            role="candidate",
            academic_status="Currently Studying",
            college="Massachusetts Institute of Technology",
            domain="MCA",
            department="Computer Applications",
            year_of_study="2nd Year",
            id_verified=True,
        )
        new_student.set_password("SecurePass123!")
        db.session.add(new_student)
        db.session.commit()

        saved = User.query.filter_by(email=test_email).first()
        assert saved is not None
        assert saved.domain == "MCA"
        assert saved.academic_status == "Currently Studying"
        assert saved.college == "Massachusetts Institute of Technology"
        assert saved.year_of_study == "2nd Year"

        # Check eligibility for newly registered student
        mca_el, _ = mca_exam.is_eligible(saved)
        cse_el, _ = cse_exam.is_eligible(saved)
        assert mca_el is True
        assert cse_el is False
        print(f"Newly registered student eligibility: MCA={mca_el}, CSE={cse_el}")

        # Clean up test student
        db.session.delete(saved)
        db.session.commit()
        print("Test student cleaned up.")

        print("\n=== ALL SYSTEM TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
