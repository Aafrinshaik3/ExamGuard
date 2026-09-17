"""LangChain AI integrity report agent with template fallback."""
import os
from typing import Dict, Any


def _template(data: Dict[str, Any]) -> str:
    name = data.get("candidate_name", "Candidate")
    score = data.get("score", 0)
    risk = data.get("risk_label", "Unknown")
    tabs = data.get("tab_switch_count", 0)
    focus = data.get("focus_loss_count", 0)
    absent = data.get("face_absent_seconds", 0)
    multi = data.get("multi_face_count", 0)
    audio = data.get("audio_spike_count", 0)

    mins, secs = divmod(absent, 60)
    parts = [f"{name} completed the examination session."]
    if tabs:
        parts.append(f"Recorded {tabs} tab-switch event(s).")
    if focus:
        parts.append(f"Focus was lost {focus} time(s).")
    if absent:
        parts.append(f"Face was absent for {mins}m {secs}s total.")
    if multi:
        parts.append(f"Multiple faces detected on {multi} occasion(s).")
    if audio:
        parts.append(f"Detected {audio} elevated audio spike(s).")
    if not any([tabs, focus, absent, multi, audio]):
        parts.append("No significant integrity events were recorded.")
    parts.append(f"Overall integrity score: {score}/100 — Risk: {risk}.")
    return " ".join(parts)


def generate_integrity_report(session_data: Dict[str, Any]) -> Dict[str, str]:
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not key or key == "your-openai-api-key-here":
        return {"summary_text": _template(session_data), "model_used": "template"}

    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema import StrOutputParser

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=key)
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an impartial academic integrity assistant. "
             "Write a concise 3-5 sentence professional summary for the invigilator. "
             "State facts only; do not accuse. End with the risk label."),
            ("human",
             "Candidate: {candidate_name}\nScore: {score}/100\nRisk: {risk_label}\n"
             "Tab switches: {tab_switch_count}\nFocus loss: {focus_loss_count}\n"
             "Face absent (s): {face_absent_seconds}\nMulti-face: {multi_face_count}\n"
             "Audio spikes: {audio_spike_count}\nFlagged: {flagged_reasons}\n\n"
             "Write the summary."),
        ])
        chain = prompt | llm | StrOutputParser()
        text = chain.invoke({
            "candidate_name": session_data.get("candidate_name", "Candidate"),
            "score": session_data.get("score", 0),
            "risk_label": session_data.get("risk_label", "Unknown"),
            "tab_switch_count": session_data.get("tab_switch_count", 0),
            "focus_loss_count": session_data.get("focus_loss_count", 0),
            "face_absent_seconds": session_data.get("face_absent_seconds", 0),
            "multi_face_count": session_data.get("multi_face_count", 0),
            "audio_spike_count": session_data.get("audio_spike_count", 0),
            "flagged_reasons": ", ".join(session_data.get("flagged_reasons", [])) or "None",
        })
        return {"summary_text": text.strip(), "model_used": "gpt-3.5-turbo"}
    except Exception as exc:
        return {
            "summary_text": _template(session_data) + f" (LLM unavailable: {type(exc).__name__})",
            "model_used": "template-fallback",
        }
