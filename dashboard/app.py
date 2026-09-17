"""ExamGuard Streamlit analytics dashboard — reads LIVE SQLite data for all students."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import json
import sqlite3

st.set_page_config(page_title="ExamGuard Analytics", page_icon="🛡️", layout="wide")

DB_PATH = ROOT / "data" / "examguard.db"
EXPORT_DIR = ROOT / "data" / "exports"


def _connect():
    if not DB_PATH.exists():
        return None
    return sqlite3.connect(str(DB_PATH))


@st.cache_data(ttl=15)
def load_scores():
    """Load every exam attempt from SQLite (all students). Fallback to CSV."""
    conn = _connect()
    if conn is not None:
        try:
            q = """
            SELECT
                s.id AS session_id,
                s.candidate_id,
                u.full_name AS candidate_name,
                u.email AS candidate_email,
                s.exam_title,
                s.status,
                s.started_at,
                s.ended_at,
                s.duration_minutes,
                i.score,
                i.risk_label,
                COALESCE(i.tab_switch_count, 0) AS tab_switch_count,
                COALESCE(i.focus_loss_count, 0) AS focus_loss_count,
                COALESCE(i.face_absent_seconds, 0) AS face_absent_seconds,
                COALESCE(i.multi_face_count, 0) AS multi_face_count,
                COALESCE(i.audio_spike_count, 0) AS audio_spike_count,
                COALESCE(i.face_presence_ratio, 1.0) AS face_presence_ratio
            FROM exam_sessions s
            LEFT JOIN users u ON u.id = s.candidate_id
            LEFT JOIN integrity_scores i ON i.session_id = s.id
            ORDER BY s.created_at DESC
            """
            df = pd.read_sql_query(q, conn)
            conn.close()
            if not df.empty:
                for col in ("started_at", "ended_at"):
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                return df
            conn.close()
        except Exception as e:
            try:
                conn.close()
            except Exception:
                pass
            st.sidebar.warning(f"DB read note: {e}")

    # Fallback: CSV exports
    p = EXPORT_DIR / "integrity_scores.csv"
    if p.exists():
        df = pd.read_csv(p)
        for col in ("started_at", "ended_at"):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df
    return pd.DataFrame()


@st.cache_data(ttl=15)
def load_events():
    conn = _connect()
    if conn is not None:
        try:
            df = pd.read_sql_query(
                "SELECT id, session_id, event_type, severity, timestamp, "
                "duration_seconds, details, is_flagged FROM event_logs ORDER BY timestamp",
                conn,
            )
            conn.close()
            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                return df
        except Exception:
            try:
                conn.close()
            except Exception:
                pass
    p = EXPORT_DIR / "session_logs.csv"
    if p.exists():
        df = pd.read_csv(p)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    return pd.DataFrame()


@st.cache_data(ttl=15)
def load_ai():
    conn = _connect()
    if conn is not None:
        try:
            df = pd.read_sql_query(
                "SELECT session_id, summary_text, model_used, generated_at FROM ai_reports",
                conn,
            )
            conn.close()
            if not df.empty:
                return df
        except Exception:
            try:
                conn.close()
            except Exception:
                pass
    p = EXPORT_DIR / "ai_reports.json"
    if p.exists():
        with open(p) as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame()


def refresh_exports():
    """Push current DB rows out to CSV/JSON for download buttons."""
    try:
        from app import create_app
        from app.services.export_data import export_analytics_data
        app = create_app()
        with app.app_context():
            return export_analytics_data()
    except Exception as e:
        return {"error": str(e)}


# ---------- UI ----------
st.sidebar.title("ExamGuard Analytics")
st.sidebar.caption("Live data from examguard.db")

if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    result = refresh_exports()
    if result and "error" not in result:
        st.sidebar.success(f"Synced {result.get('sessions', 0)} sessions")
    st.rerun()

scores = load_scores()
events = load_events()
ai = load_ai()

if scores.empty:
    st.warning(
        "No exam data found yet.\n\n"
        "1. Run the Flask app and have students complete exams, **or**\n"
        "2. Run `python scripts/generate_synthetic_data.py` for demo data.\n\n"
        f"Looking for DB at: `{DB_PATH}`"
    )
    st.stop()

# Scored subset (has integrity score) vs all attempts
scored = scores[scores["score"].notna()].copy() if "score" in scores.columns else scores.copy()

page = st.sidebar.radio(
    "Go to",
    ["Overview", "All students", "Scores", "Events", "Clustering", "Risk", "Drill-down", "Exports"],
)

if page == "Overview":
    st.title("Cohort overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total attempts", len(scores))
    c2.metric("Unique students", int(scores["candidate_id"].nunique()) if "candidate_id" in scores.columns else 0)
    c3.metric("Scored sessions", len(scored))
    if not scored.empty:
        c4.metric("Avg score", f"{scored['score'].mean():.1f}")
        c5.metric("High risk", int((scored["risk_label"] == "High").sum()))
    else:
        c4.metric("Avg score", "—")
        c5.metric("High risk", 0)

    if not scored.empty and "risk_label" in scored.columns:
        rc = scored["risk_label"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
        fig = px.pie(
            names=rc.index, values=rc.values, color=rc.index,
            color_discrete_map={"Low": "#16a34a", "Medium": "#d97706", "High": "#dc2626"},
            hole=0.4, title="Risk distribution (scored sessions)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Latest attempts (all students)")
    cols = [c for c in ["session_id", "candidate_name", "candidate_email", "exam_title", "status", "score", "risk_label", "started_at"] if c in scores.columns]
    st.dataframe(scores[cols].head(30), use_container_width=True)

elif page == "All students":
    st.title("All students who attempted exams")
    st.markdown("Every session stored in the database — submitted, terminated, or still active.")

    # Per-student summary
    if "candidate_id" in scores.columns:
        agg = {
            "session_id": "count",
            "score": "mean",
        }
        if "tab_switch_count" in scores.columns:
            agg["tab_switch_count"] = "sum"
        if "face_absent_seconds" in scores.columns:
            agg["face_absent_seconds"] = "sum"

        student_summary = (
            scores.groupby(["candidate_id", "candidate_name", "candidate_email"], dropna=False)
            .agg(**{
                "attempts": ("session_id", "count"),
                "avg_score": ("score", "mean"),
                "exams": ("exam_title", lambda s: ", ".join(sorted(set(str(x) for x in s if pd.notna(x))))),
            })
            .reset_index()
            .sort_values("attempts", ascending=False)
        )
        st.subheader("Per-student summary")
        st.dataframe(student_summary, use_container_width=True)

    st.subheader("Full session list")
    show_cols = [c for c in [
        "session_id", "candidate_name", "candidate_email", "exam_title", "status",
        "score", "risk_label", "tab_switch_count", "face_absent_seconds",
        "multi_face_count", "started_at", "ended_at",
    ] if c in scores.columns]
    st.dataframe(scores[show_cols], use_container_width=True)
    st.caption(f"Showing **{len(scores)}** session(s) from **{scores['candidate_id'].nunique() if 'candidate_id' in scores.columns else '—'}** student(s).")

elif page == "Scores":
    st.title("Integrity scores")
    if scored.empty:
        st.info("No scored sessions yet. Students must submit (or be auto-terminated with a generated report).")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            sns.histplot(scored["score"].dropna(), bins=12, kde=True, ax=ax, color="#2563eb")
            ax.set_xlabel("Integrity score")
            st.pyplot(fig)
        with col2:
            fig = px.box(
                scored, x="risk_label", y="score", color="risk_label",
                color_discrete_map={"Low": "#16a34a", "Medium": "#d97706", "High": "#dc2626"},
                category_orders={"risk_label": ["Low", "Medium", "High"]},
            )
            st.plotly_chart(fig, use_container_width=True)
        fig = px.scatter(
            scored, x="tab_switch_count", y="score", size="face_absent_seconds",
            color="risk_label", hover_data=["candidate_name", "exam_title"],
            color_discrete_map={"Low": "#16a34a", "Medium": "#d97706", "High": "#dc2626"},
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            scored.sort_values("score")[
                [c for c in ["session_id", "candidate_name", "exam_title", "score", "risk_label", "tab_switch_count", "face_absent_seconds"] if c in scored.columns]
            ],
            use_container_width=True,
        )

elif page == "Events":
    st.title("Event analytics")
    if events.empty:
        st.info("No events logged yet.")
    else:
        tc = events["event_type"].value_counts()
        st.plotly_chart(px.bar(x=tc.index, y=tc.values, labels={"x": "Type", "y": "Count"}), use_container_width=True)
        ev = events.copy()
        if "timestamp" in ev.columns:
            ev["day"] = ev["timestamp"].dt.date
            pivot = ev.groupby(["day", "event_type"]).size().unstack(fill_value=0)
            if not pivot.empty:
                fig, ax = plt.subplots(figsize=(10, 3.5))
                sns.heatmap(pivot.T, cmap="YlOrRd", ax=ax)
                st.pyplot(fig)
        st.metric("Flagged events", int(events["is_flagged"].sum()) if "is_flagged" in events.columns else 0)
        st.dataframe(events.tail(100), use_container_width=True)

elif page == "Clustering":
    st.title("Behaviour clustering (K-Means)")
    st.markdown(
        "K-Means groups **scored** sessions by proctoring behaviour "
        "(tab switches, face absence, etc.) for invigilator review."
    )
    if scored.empty or len(scored) < 2:
        st.info("Need at least 2 scored sessions to run clustering.")
    else:
        feats = ["tab_switch_count", "focus_loss_count", "face_absent_seconds", "multi_face_count", "face_presence_ratio"]
        if "audio_spike_count" in scored.columns:
            feats.append("audio_spike_count")
        available = [f for f in feats if f in scored.columns]
        X = StandardScaler().fit_transform(scored[available].fillna(0))
        k_max = min(5, len(scored))
        k = st.slider("Number of behaviour clusters (k)", 2, k_max, min(3, k_max))
        work = scored.copy()
        work["cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)

        summary = work.groupby("cluster")[available + ["score"]].mean()

        def label_row(row):
            tabs = row.get("tab_switch_count", 0)
            face = row.get("face_absent_seconds", 0)
            if tabs <= 1 and face <= 30:
                return "Clean / focused"
            if tabs >= 4 or face >= 120:
                return "High distraction / risk"
            return "Moderate issues"

        cluster_labels = summary.apply(label_row, axis=1).to_dict()
        work["behaviour_profile"] = work["cluster"].map(cluster_labels)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                px.scatter(
                    work, x="tab_switch_count", y="face_absent_seconds",
                    color="behaviour_profile", size="score",
                    hover_data=["candidate_name", "risk_label", "cluster"],
                    title="Tab switches vs face-absent time",
                ),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                px.scatter(
                    work, x="tab_switch_count", y="score",
                    color="behaviour_profile",
                    hover_data=["candidate_name", "face_absent_seconds"],
                    title="Tab switches vs integrity score",
                ),
                use_container_width=True,
            )

        st.subheader("Cluster averages")
        st.dataframe(summary.round(2), use_container_width=True)

        out = EXPORT_DIR / "cluster_assignments.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        cols = [c for c in ["session_id", "candidate_name", "cluster", "behaviour_profile", "score", "risk_label", "tab_switch_count", "face_absent_seconds"] if c in work.columns]
        work[cols].to_csv(out, index=False)
        st.success("Saved cluster_assignments.csv")

elif page == "Risk":
    st.title("Risk profiling")
    if scored.empty:
        st.info("No scored sessions yet.")
    else:
        order = ["Low", "Medium", "High"]
        rc = scored["risk_label"].value_counts().reindex(order).fillna(0)
        st.plotly_chart(
            px.bar(x=rc.index, y=rc.values, color=rc.index,
                   color_discrete_map={"Low": "#16a34a", "Medium": "#d97706", "High": "#dc2626"}),
            use_container_width=True,
        )
        high = scored[scored["risk_label"] == "High"].sort_values("score")
        st.subheader("High-risk sessions")
        st.dataframe(
            high[[c for c in ["session_id", "candidate_name", "exam_title", "score", "tab_switch_count", "face_absent_seconds"] if c in high.columns]],
            use_container_width=True,
        )

elif page == "Drill-down":
    st.title("Session drill-down")
    options = scores["session_id"].tolist()
    labels = {
        int(r.session_id): f"#{int(r.session_id)} — {r.candidate_name} — {r.exam_title} ({r.status})"
        for r in scores.itertuples()
    }
    sid = st.selectbox("Session", options, format_func=lambda x: labels.get(int(x), str(x)))
    row = scores[scores["session_id"] == sid].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{row['score']:.1f}" if pd.notna(row.get("score")) else "—")
    c2.metric("Risk", row["risk_label"] if pd.notna(row.get("risk_label")) and row.get("risk_label") else "—")
    c3.metric("Candidate", row.get("candidate_name", "—"))
    c4.metric("Status", row.get("status", "—"))
    if not ai.empty:
        r = ai[ai["session_id"] == sid]
        if not r.empty:
            st.info(r.iloc[0]["summary_text"])
    if not events.empty:
        st.subheader("Events for this session")
        st.dataframe(
            events[events["session_id"] == sid].sort_values("timestamp"),
            use_container_width=True,
        )

else:
    st.title("Exports")
    if st.button("Rebuild export files from database"):
        st.cache_data.clear()
        result = refresh_exports()
        if result and "error" not in result:
            st.success(f"Exported {result.get('sessions', 0)} sessions, {result.get('events', 0)} events.")
        else:
            st.error(result.get("error", "Export failed") if result else "Export failed")

    for fn in ["integrity_scores.csv", "session_logs.csv", "ai_reports.json", "cluster_assignments.csv"]:
        p = EXPORT_DIR / fn
        if p.exists():
            st.download_button(f"Download {fn}", p.read_bytes(), fn, key=fn)
        else:
            st.write(f"⏳ {fn} — not generated yet (click rebuild or run clustering / complete an exam)")
