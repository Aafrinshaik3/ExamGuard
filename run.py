"""ExamGuard – Unified Application Entry Point.

Runs both the Student Portal & Admin/Invigilator Console (Flask)
and the Analytics Engine (Streamlit) concurrently under a single command.
"""
import os
import sys
import argparse
import subprocess
import atexit
from pathlib import Path

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from app import create_app
from app.routes.exam import ensure_exam_catalog

streamlit_process = None


def cleanup():
    global streamlit_process
    if streamlit_process and streamlit_process.poll() is None:
        try:
            streamlit_process.terminate()
            streamlit_process.wait(timeout=2)
        except Exception:
            try:
                streamlit_process.kill()
            except Exception:
                pass


atexit.register(cleanup)


def start_streamlit(port=8501):
    global streamlit_process
    dashboard_script = Path(__file__).resolve().parent / "dashboard" / "app.py"
    if not dashboard_script.exists():
        return None
    try:
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(dashboard_script),
            "--server.port",
            str(port),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ]
        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NEW_PROCESS_GROUP
        streamlit_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
        )
        return streamlit_process
    except Exception as e:
        print(f"[!] Warning: Could not auto-start Streamlit: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="ExamGuard Unified Server")
    parser.add_argument("--port", type=int, default=5000, help="Port for Flask app (default: 5000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--flask-only", action="store_true", help="Only run Flask (do not start Streamlit)")
    parser.add_argument("--streamlit-only", action="store_true", help="Only run Streamlit dashboard")
    parser.add_argument("--streamlit-port", type=int, default=8501, help="Port for Streamlit (default: 8501)")
    parser.add_argument("--no-debug", action="store_true", help="Disable Flask debug mode")
    args = parser.parse_args()

    app = create_app()

    with app.app_context():
        ensure_exam_catalog()

    if args.streamlit_only:
        print("\nStarting ExamGuard Streamlit Analytics Dashboard...")
        dashboard_script = Path(__file__).resolve().parent / "dashboard" / "app.py"
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(dashboard_script),
            "--server.port",
            str(args.streamlit_port),
        ])
        return

    st_started = False
    if not args.flask_only:
        proc = start_streamlit(port=args.streamlit_port)
        if proc:
            st_started = True

    print("\n" + "=" * 76)
    print(" 🛡️  ExamGuard — Online Examination & Automated Proctoring Platform")
    print("=" * 76)
    print(f" 🎓 Student Portal:        http://localhost:{args.port}/student  (or /)")
    print(f" 👨‍🏫 Admin & Invigilator:  http://localhost:{args.port}/admin    (or /invigilator)")
    if st_started:
        print(f" 📊 Streamlit Analytics:   http://localhost:{args.streamlit_port} (Auto-started in background)")
    print("=" * 76)
    print(" Proctoring: Webcam face presence · Microphone levels · Tab / focus tracking")
    print(" Catalog: Multi-domain exams (B.Tech, CSE, MCA, BA, Foundation) · Native analytics")
    print(" Press Ctrl+C to stop both servers.")
    print("=" * 76 + "\n")

    try:
        app.run(host=args.host, port=args.port, debug=not args.no_debug, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


if __name__ == "__main__":
    main()
