"""
Migration and Database Cleanup:
1. Adds missing columns to SQLite tables (users, available_exams).
2. Deletes demo users (candidate001-035 and invigilator1-2) and their associated sessions, scores, logs, and reports.
3. Sets default profile data for genuine users.
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "examguard.db"

def migrate():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Inspect and update 'users' table columns
    cursor.execute("PRAGMA table_info(users)")
    existing_user_cols = {row[1] for row in cursor.fetchall()}
    print(f"Existing columns in users: {existing_user_cols}")

    user_cols_to_add = [
        ("academic_status", "VARCHAR(50) DEFAULT 'Currently Studying'"),
        ("college", "VARCHAR(200) DEFAULT ''"),
        ("domain", "VARCHAR(100) DEFAULT ''"),
        ("department", "VARCHAR(120) DEFAULT ''"),
        ("year_of_study", "VARCHAR(50) DEFAULT ''"),
    ]

    for col_name, col_type in user_cols_to_add:
        if col_name not in existing_user_cols:
            print(f"Adding column '{col_name}' to users table...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")

    # 2. Inspect and update 'available_exams' table columns
    cursor.execute("PRAGMA table_info(available_exams)")
    existing_exam_cols = {row[1] for row in cursor.fetchall()}
    print(f"Existing columns in available_exams: {existing_exam_cols}")

    exam_cols_to_add = [
        ("target_domain", "VARCHAR(100) DEFAULT 'All'"),
        ("target_department", "VARCHAR(120) DEFAULT 'All'"),
        ("target_year", "VARCHAR(100) DEFAULT 'All'"),
        ("target_status", "VARCHAR(100) DEFAULT 'All'"),
    ]

    for col_name, col_type in exam_cols_to_add:
        if col_name not in existing_exam_cols:
            print(f"Adding column '{col_name}' to available_exams table...")
            cursor.execute(f"ALTER TABLE available_exams ADD COLUMN {col_name} {col_type}")

    conn.commit()

    # 3. Clean up demo users and demo invigilators
    cursor.execute("""
        SELECT id, email, full_name, role FROM users 
        WHERE email LIKE 'candidate%@student.edu' 
           OR email LIKE 'invigilator%@examguard.edu'
           OR email LIKE '%demo%'
    """)
    demo_users = cursor.fetchall()
    print(f"Found {len(demo_users)} demo users to remove.")

    if demo_users:
        demo_ids = [u[0] for u in demo_users]
        demo_ids_placeholder = ",".join("?" for _ in demo_ids)

        # Get sessions for these demo users
        cursor.execute(
            f"SELECT id FROM exam_sessions WHERE candidate_id IN ({demo_ids_placeholder})",
            demo_ids
        )
        demo_sessions = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(demo_sessions)} sessions associated with demo users.")

        if demo_sessions:
            sess_placeholder = ",".join("?" for _ in demo_sessions)
            cursor.execute(f"DELETE FROM event_logs WHERE session_id IN ({sess_placeholder})", demo_sessions)
            cursor.execute(f"DELETE FROM integrity_scores WHERE session_id IN ({sess_placeholder})", demo_sessions)
            cursor.execute(f"DELETE FROM ai_reports WHERE session_id IN ({sess_placeholder})", demo_sessions)
            cursor.execute(f"DELETE FROM exam_sessions WHERE id IN ({sess_placeholder})", demo_sessions)
            print("Deleted demo event_logs, integrity_scores, ai_reports, and exam_sessions.")

        # Delete the demo users themselves
        cursor.execute(f"DELETE FROM users WHERE id IN ({demo_ids_placeholder})", demo_ids)
        print("Deleted demo users from users table.")

    # 4. Set defaults for genuine users if not set
    cursor.execute("SELECT id, email, role, full_name, domain, college FROM users")
    remaining_users = cursor.fetchall()
    print(f"Remaining genuine users in database: {remaining_users}")

    for uid, email, role, name, dom, col in remaining_users:
        if role == "candidate":
            cursor.execute("""
                UPDATE users 
                SET academic_status = COALESCE(NULLIF(academic_status, ''), 'Currently Studying'),
                    college = COALESCE(NULLIF(college, ''), 'University College of Engineering'),
                    domain = COALESCE(NULLIF(domain, ''), 'B.Tech'),
                    department = COALESCE(NULLIF(department, ''), 'Computer Science & Engineering (CSE)'),
                    year_of_study = COALESCE(NULLIF(year_of_study, ''), '4th Year')
                WHERE id = ?
            """, (uid,))
        elif role in ("invigilator", "admin"):
            cursor.execute("""
                UPDATE users 
                SET academic_status = 'Faculty / Invigilator',
                    college = COALESCE(NULLIF(college, ''), 'University Examination Authority'),
                    domain = COALESCE(NULLIF(domain, ''), 'Faculty of Engineering & Technology'),
                    department = COALESCE(NULLIF(department, ''), 'Department of Computer Science & Engineering'),
                    year_of_study = 'Faculty Staff'
                WHERE id = ?
            """, (uid,))

    conn.commit()
    conn.close()
    print("Migration and database cleanup complete successfully!")

if __name__ == "__main__":
    migrate()
