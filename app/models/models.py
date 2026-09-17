"""SQLAlchemy models for ExamGuard."""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="candidate")
    photo_path = db.Column(db.String(255))
    id_type = db.Column(db.String(40))
    id_number = db.Column(db.String(80))
    id_document_path = db.Column(db.String(255))
    id_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Academic & Institution details
    academic_status = db.Column(db.String(50), default="Currently Studying")  # Currently Studying / Graduated / Beginner
    college = db.Column(db.String(200), default="")
    domain = db.Column(db.String(100), default="")  # B.Tech, MCA, BA, B.Sc, etc.
    department = db.Column(db.String(120), default="")  # CSE, ECE, Economics, Computer Applications, etc.
    year_of_study = db.Column(db.String(50), default="")  # 1st Year, 2nd Year, 3rd Year, 4th Year, Graduated, Beginner

    sessions = db.relationship("ExamSession", backref="candidate", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_profile_complete(self) -> bool:
        return bool(self.photo_path and self.id_document_path and self.id_verified)


class AvailableExam(db.Model):
    """Catalog of tests shown on the candidate dashboard."""
    __tablename__ = "available_exams"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    duration_minutes = db.Column(db.Integer, default=60)
    total_questions = db.Column(db.Integer, default=10)
    subject = db.Column(db.String(80), default="General")
    target_domain = db.Column(db.String(100), default="All")  # B.Tech, MCA, BA, All, etc.
    target_department = db.Column(db.String(120), default="All")  # CSE, ECE, Economics, All, etc.
    target_year = db.Column(db.String(100), default="All")  # 1st Year, 2nd Year, etc., or All
    target_status = db.Column(db.String(100), default="All")  # Currently Studying, Graduated, Beginner, All
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_eligible(self, user) -> tuple:
        """
        Check if the given user is eligible to take this exam.
        Returns: (is_eligible: bool, message: str)
        """
        if not user or not getattr(user, "is_authenticated", False):
            return False, "Login required"

        if getattr(user, "role", "") in ("admin", "invigilator"):
            return True, "Authorized (Faculty / Proctor Preview)"

        u_status = (getattr(user, "academic_status", "") or "").strip()
        u_domain = (getattr(user, "domain", "") or "").strip()
        u_dept = (getattr(user, "department", "") or "").strip()
        u_year = (getattr(user, "year_of_study", "") or "").strip()

        tgt_domain = (self.target_domain or "All").strip()
        tgt_dept = (self.target_department or "All").strip()
        tgt_year = (self.target_year or "All").strip()
        tgt_status = (self.target_status or "All").strip()

        # Open / General assessments (open to all degrees and beginners)
        if tgt_domain.lower() in ("all", "general", "any") and tgt_dept.lower() in ("all", "any"):
            return True, "Open assessment — available to all domains"

        # Beginner student
        if u_status.lower() == "beginner":
            if "beginner" in tgt_status.lower() or tgt_domain.lower() in ("all", "general"):
                return True, "Eligible for Beginner / Foundation level"
            return False, f"Degree curriculum exam ({tgt_domain} · {tgt_dept}). Recommended for enrolled/graduated students."

        # Domain verification (B.Tech, MCA, BA, etc.)
        if tgt_domain.lower() not in ("all", "any"):
            if tgt_domain.lower() not in u_domain.lower() and u_domain.lower() not in tgt_domain.lower():
                return False, f"Domain restricted: Requires {tgt_domain} (Your registered domain: {u_domain or 'Not set'})"

        # Department verification
        if tgt_dept.lower() not in ("all", "any"):
            dept_matches = False
            if tgt_dept.lower() in u_dept.lower() or u_dept.lower() in tgt_dept.lower():
                dept_matches = True
            acronym_map = {
                "cse": ["computer science", "cse"],
                "ece": ["electronics", "ece"],
                "ai & data science": ["artificial intelligence", "data science", "ai", "ai & ds"],
                "eee": ["electrical", "eee"],
                "mechanical": ["mechanical", "mech"],
                "computer applications": ["computer applications", "mca", "software development"],
                "english": ["english", "literature"],
                "economics": ["economics", "economy"],
                "political science": ["political", "politics", "constitution"],
                "history": ["history", "civilization"],
                "psychology": ["psychology", "behavior"],
            }
            tgt_lower = tgt_dept.lower()
            for k, syns in acronym_map.items():
                if any(s in tgt_lower for s in syns) and any(s in u_dept.lower() for s in syns):
                    dept_matches = True
                    break

            if not dept_matches:
                return False, f"Department restricted: Requires {tgt_dept} (Your department: {u_dept or 'Not set'})"

        # Year of study verification
        if tgt_year.lower() not in ("all", "any"):
            if u_year and tgt_year.lower() not in u_year.lower() and u_year.lower() not in tgt_year.lower():
                return False, f"Year restricted: Requires {tgt_year} (You are {u_year})"

        return True, f"Eligible for {u_domain} · {u_dept} students"


class ExamSession(db.Model):
    __tablename__ = "exam_sessions"
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("available_exams.id"), nullable=True)
    exam_title = db.Column(db.String(200), default="Online Assessment")
    status = db.Column(db.String(20), default="registered")
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer, default=60)
    test_score = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exam = db.relationship("AvailableExam", backref="sessions")
    events = db.relationship("EventLog", backref="session", lazy="dynamic", cascade="all, delete-orphan")
    integrity_score = db.relationship("IntegrityScore", backref="session", uselist=False, cascade="all, delete-orphan")
    ai_report = db.relationship("AIReport", backref="session", uselist=False, cascade="all, delete-orphan")


class EventLog(db.Model):
    __tablename__ = "event_logs"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), default="info")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    duration_seconds = db.Column(db.Integer, default=0)
    details = db.Column(db.Text)
    is_flagged = db.Column(db.Boolean, default=False)


class IntegrityScore(db.Model):
    __tablename__ = "integrity_scores"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), unique=True, nullable=False)
    score = db.Column(db.Float, nullable=False)
    risk_label = db.Column(db.String(20), nullable=False)
    tab_switch_count = db.Column(db.Integer, default=0)
    focus_loss_count = db.Column(db.Integer, default=0)
    face_absent_seconds = db.Column(db.Integer, default=0)
    multi_face_count = db.Column(db.Integer, default=0)
    audio_spike_count = db.Column(db.Integer, default=0)
    face_presence_ratio = db.Column(db.Float, default=1.0)
    computed_at = db.Column(db.DateTime, default=datetime.utcnow)


class AIReport(db.Model):
    __tablename__ = "ai_reports"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), unique=True, nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    model_used = db.Column(db.String(50), default="template")
