"""Test Flask endpoints, template rendering, and demo route elimination."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app, db
from app.models.models import User

def test_routes():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()

    with app.app_context():
        # 1. Check portal gateway
        resp = client.get("/portal")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Demo Student" not in html
        assert "demo_login" not in html
        print("[OK] Portal gateway renders cleanly without demo buttons.")

        # 2. Check login page
        resp = client.get("/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "demo-box" not in html
        assert "demo_login" not in html
        print("[OK] Login page renders cleanly without demo buttons.")

        # 3. Check demo-login route is deleted (should return 404)
        resp = client.get("/demo-login/candidate")
        assert resp.status_code == 404
        print("[OK] /demo-login/candidate returns 404 as expected.")

        # 4. Check registration page has new fields
        resp = client.get("/register")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "academic_status" in html
        assert "college" in html
        assert "domain" in html
        assert "department" in html
        assert "year_of_study" in html
        print("[OK] Registration page has all required academic profile fields.")

        # 5. Test candidate login and dashboard rendering
        candidate = User.query.filter_by(role="candidate").first()
        candidate.set_password("TestCandidate123!")
        db.session.commit()

        login_resp = client.post("/login", data={"email": candidate.email, "password": "TestCandidate123!"}, follow_redirects=True)
        assert login_resp.status_code == 200

        resp = client.get("/student")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert candidate.full_name in html
        assert candidate.domain in html
        assert candidate.college in html
        assert "Eligible to Take" in html
        print("[OK] Student Dashboard renders candidate details and eligibility badges successfully.")

        # 6. Test admin login and dashboard rendering
        client.get("/logout")
        admin = User.query.filter(User.role.in_(["invigilator", "admin"])).first()
        admin.set_password("TestAdmin123!")
        db.session.commit()

        admin_login_resp = client.post("/login", data={"email": admin.email, "password": "TestAdmin123!"}, follow_redirects=True)
        assert admin_login_resp.status_code == 200

        resp = client.get("/admin")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert admin.full_name in html
        assert "Faculty &amp; Invigilators Directory" in html or "Faculty & Invigilators Directory" in html
        assert "Active Proctor" in html
        print("[OK] Admin & Invigilator Console renders invigilator details successfully.")

        # 7. Test students roster in admin
        resp = client.get("/admin/students")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Candidate Directory" in html
        assert candidate.college in html
        print("[OK] Admin Students roster displays candidate academic credentials successfully.")

        print("\n=== ALL FLASK ROUTE AND TEMPLATE TESTS PASSED! ===")

if __name__ == "__main__":
    test_routes()
