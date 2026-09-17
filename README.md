# ExamGuard — Online Exam Monitoring & Integrity Analytics

Professional online examination platform with **face presence monitoring**, **voice/audio level detection**, **tab/focus tracking**, **ID verification**, rule-based integrity scoring, and AI-generated reports.

---

## 🌟 Dual Portals: Student & Admin Sides

ExamGuard features two distinct, dedicated environments:

### 🎓 Student Portal (`http://localhost:5000/student` or `/`)
- **Webcam Face Registration**: Reference face capture used for ongoing identity match during exams.
- **ID Verification**: Aadhaar, College ID, Passport upload and verification.
- **Live Proctored Exams**:
  - Continuous MediaPipe & OpenCV face presence monitoring (detects absence, multiple faces, face mismatches).
  - Web Audio API microphone volume analysis (detects voice, speech, background coaching).
  - Tab-switching & window focus tracking with strict violation counters.
  - Automatic session termination on excessive violations.
- **Attendance & Results**: History of attended exams and detailed integrity reports.

### 🛡️ Admin & Invigilator Console (`http://localhost:5000/admin` or `/invigilator`)
- **Live Proctoring Room (`/admin/live`)**:
  - Real-time grid of all active students currently writing exams.
  - Live **Voice / Audio Status** (detects speech & audio spikes instantly).
  - Live **Face Presence Status** (checks face visible vs. absent vs. multi-face).
  - Violation tallies (tab switches, face absences, audio spikes).
  - Real-time streaming alert feed auto-polling every 3 seconds.
  - One-click remote exam termination.
- **Candidate Roster & ID Verification (`/admin/students`)**:
  - Review webcam photos, uploaded government IDs, and approve or revoke verification.
- **Assessment Management (`/admin/exams`)**:
  - Create new exams, configure duration and question counts, toggle test availability.
- **Analytics Dashboard (`/admin/analytics`)** — **native Flask, no Streamlit required**:
  - Dark UI matching the cohort analytics layout (risk donut, category scores, latest attempts).
  - Full pages: Overview · All students · Scores · Events · Clustering (K-Means) · Risk · Drill-down · Exports.
  - Live data from `examguard.db`; CSV/JSON downloads from the same page.

---

## 🚀 Quick Start (Single Command)

You no longer need to switch commands or run multiple terminals. A single command launches everything:

```bash
# 1. Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# 2. Run ExamGuard (launches both Student & Admin portals and auto-starts Streamlit)
python run.py
```

### Server Endpoints:
- **Portal Gateway (Selection)**: [http://localhost:5000/](http://localhost:5000/)
- **Student Portal**: [http://localhost:5000/student](http://localhost:5000/student)
- **Admin Console**: [http://localhost:5000/admin](http://localhost:5000/admin)
- **Live Proctoring Feed**: [http://localhost:5000/admin/live](http://localhost:5000/admin/live)
- **Native Analytics (no Streamlit)**: [http://localhost:5000/admin/analytics](http://localhost:5000/admin/analytics)

> **Note:** Full analytics (Overview, Scores, Events, Clustering, Risk, Drill-down, Exports) run inside Flask at `/admin/analytics`. You do **not** need to start Streamlit. Optional legacy Streamlit remains at `dashboard/app.py` if you still want it.

### CLI Options:
```bash
python run.py                       # Flask (and optional Streamlit if configured)
python run.py --flask-only          # Run only Flask (port 5000) — recommended
python run.py --streamlit-only      # Run only legacy Streamlit (port 8501)
python run.py --port 8000           # Run Flask on custom port
```

---

## ⚡ Demo Accounts

1-click login buttons are available on the login page, or use these credentials:

| Portal | Role | Email | Password |
|---|---|---|---|
| **Student Portal** | Candidate | `candidate001@student.edu` | `candidate123` |
| **Admin Console** | Invigilator / Admin | `invigilator1@examguard.edu` | `invigilator123` |

> [!TIP]
> **Creating New Admin Accounts**:
> You can also register directly as an Admin on the registration page by selecting **Admin Registration** and entering the default passkey `admin123`.

---

## 🛠️ Tech Stack

Flask · OpenCV · MediaPipe · Web Audio API · SQLite · LangChain · Pandas · Scikit-learn · Streamlit · Faker
