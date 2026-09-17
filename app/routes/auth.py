"""Authentication, registration & ID verification."""
import os
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.models import User
import base64
import numpy as np
import cv2

auth_bp = Blueprint("auth", __name__)

ALLOWED_ID = {"png", "jpg", "jpeg", "pdf", "webp"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_ID


@auth_bp.route("/")
@auth_bp.route("/portal")
def index():
    if current_user.is_authenticated:
        if current_user.role in ("invigilator", "admin"):
            return redirect(url_for("admin.dashboard"))
        if not current_user.is_profile_complete:
            return redirect(url_for("auth.verify_id"))
        return redirect(url_for("exam.candidate_home"))
    return render_template("portal_gateway.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    role_hint = request.args.get("role", "candidate")
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f"Welcome back, {user.full_name}!", "success")
            if user.role in ("invigilator", "admin"):
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("auth.index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", role_hint=role_hint)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    role_hint = request.args.get("role", "candidate")
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        full_name = request.form.get("full_name", "").strip()
        role = request.form.get("role", "candidate").strip().lower()
        admin_passkey = request.form.get("admin_passkey", "").strip()
        photo_data = request.form.get("photo_data", "")

        # Academic / Institution fields
        academic_status = request.form.get("academic_status", "Currently Studying").strip()
        college = request.form.get("college", "").strip()
        domain = request.form.get("domain", "").strip()
        department = request.form.get("department", "").strip()
        year_of_study = request.form.get("year_of_study", "").strip()

        if not all([email, password, full_name]):
            flash("Name, email, and password are required.", "danger")
            return redirect(url_for("auth.register", role=role))
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("auth.register", role=role))
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("auth.register", role=role))

        if role in ("invigilator", "admin"):
            expected_key = os.getenv("ADMIN_REGISTRATION_KEY", "admin123")
            if admin_passkey != expected_key:
                flash("Invalid Admin Passkey. Please enter a valid authorization key or contact administrator.", "danger")
                return redirect(url_for("auth.register", role="invigilator"))

            user = User(
                email=email,
                full_name=full_name,
                role="invigilator",
                id_verified=True,
                id_type="admin_key",
                id_number=f"ADM-{datetime.utcnow().strftime('%M%S')}",
                academic_status="Faculty / Invigilator",
                college=college or "Examination Authority",
                domain=domain or "Faculty of Academics",
                department=department or "Examination Controller",
                year_of_study="Faculty Staff",
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Invigilator / Admin account created successfully!", "success")
            return redirect(url_for("admin.dashboard"))

        # Candidate registration requires face capture
        if not photo_data or not photo_data.startswith("data:image"):
            flash("Please capture your face photo with the webcam before registering.", "danger")
            return redirect(url_for("auth.register", role="candidate"))

        user = User(
            email=email,
            full_name=full_name,
            role="candidate",
            academic_status=academic_status or "Currently Studying",
            college=college or "Not specified",
            domain=domain or "B.Tech",
            department=department or "General",
            year_of_study=year_of_study or "1st Year",
        )
        user.set_password(password)

        try:
            _, encoded = photo_data.split(",", 1)
            arr = np.frombuffer(base64.b64decode(encoded), np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                flash("Could not process the photo. Capture again.", "danger")
                return redirect(url_for("auth.register", role="candidate"))
            photos_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "photos")
            os.makedirs(photos_dir, exist_ok=True)
            fname = secure_filename(
                f"{email.replace('@', '_')}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.jpg"
            )
            path = os.path.join(photos_dir, fname)
            ok = cv2.imwrite(path, frame)
            if not ok or not os.path.isfile(path):
                flash("Could not save the photo. Try again.", "danger")
                return redirect(url_for("auth.register", role="candidate"))
            user.photo_path = f"uploads/photos/{fname}"
        except Exception as e:
            flash(f"Photo capture failed: {e}", "danger")
            return redirect(url_for("auth.register", role="candidate"))

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created with face photo and academic details. Please complete ID verification.", "success")
        return redirect(url_for("auth.verify_id"))

    return render_template("register.html", role_hint=role_hint)


@auth_bp.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    """Allows candidates or invigilators to update academic and institutional details."""
    full_name = request.form.get("full_name", "").strip()
    college = request.form.get("college", "").strip()
    academic_status = request.form.get("academic_status", "").strip()
    domain = request.form.get("domain", "").strip()
    department = request.form.get("department", "").strip()
    year_of_study = request.form.get("year_of_study", "").strip()

    if full_name:
        current_user.full_name = full_name
    if college:
        current_user.college = college
    if academic_status:
        current_user.academic_status = academic_status
    if domain:
        current_user.domain = domain
    if department:
        current_user.department = department
    if year_of_study:
        current_user.year_of_study = year_of_study

    db.session.commit()
    flash("Profile and academic details updated successfully!", "success")
    if current_user.role in ("invigilator", "admin"):
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("exam.candidate_home"))


@auth_bp.route("/verify-id", methods=["GET", "POST"])
@login_required
def verify_id():
    if current_user.is_profile_complete:
        return redirect(url_for("exam.candidate_home"))

    if request.method == "POST":
        id_type = request.form.get("id_type", "").strip()
        id_number = request.form.get("id_number", "").strip()
        file = request.files.get("id_document")

        if not id_type or not id_number:
            flash("Please select ID type and enter ID number.", "danger")
            return redirect(url_for("auth.verify_id"))
        if not file or file.filename == "":
            flash("Please upload a clear photo/scan of your ID.", "danger")
            return redirect(url_for("auth.verify_id"))
        if not _allowed(file.filename):
            flash("Allowed formats: JPG, PNG, PDF, WEBP.", "danger")
            return redirect(url_for("auth.verify_id"))

        fname = secure_filename(
            f"id_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        )
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], "ids", fname)
        file.save(path)

        current_user.id_type = id_type
        current_user.id_number = id_number
        current_user.id_document_path = f"uploads/ids/{fname}"
        # Auto-verify for demo (in production this would be manual/OCR review)
        current_user.id_verified = True
        db.session.commit()
        flash("Identity verified successfully. You may now take assessments.", "success")
        return redirect(url_for("exam.candidate_home"))

    return render_template("verify_id.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
