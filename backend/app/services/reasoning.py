"""
LLM Reasoning Layer.
Converts structured biomechanics data + transcript into clinical summaries.
Supports: Ollama (local), OpenAI, or rule-based fallback.
"""
from app.schemas.analysis import BiomechanicsResult
from app.core.config import settings


SYSTEM_PROMPT = """You are a clinical physiotherapy AI assistant.
You receive movement analysis data from video and provide:
1. A clear, concise clinical summary (2-3 sentences)
2. Specific, actionable recommendations for the patient/therapist

Be factual. Do not over-diagnose. Flag when professional assessment is needed."""


def build_prompt(biomechanics: BiomechanicsResult, transcript: str | None) -> str:
    lines = [
        "=== MOVEMENT ANALYSIS DATA ===",
        f"Risk Level: {biomechanics.risk_level.upper()}",
        f"Knee Angle (avg): {biomechanics.knee_angle}°",
        f"Hip Angle (avg): {biomechanics.hip_angle}°",
        f"Spine Deviation: {biomechanics.spine_deviation}",
        f"Asymmetry Score: {biomechanics.asymmetry_score}",
        "",
        "Detected Alerts:",
    ]
    for alert in biomechanics.alerts:
        lines.append(f"  - {alert}")

    if transcript:
        lines += ["", "=== AUDIO TRANSCRIPT ===", transcript]

    lines += ["", "Provide a clinical summary and recommendations."]
    return "\n".join(lines)


def _ollama_generate(prompt: str) -> str:
    try:
        import httpx
        response = httpx.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": settings.llm_model, "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}", "stream": False},
            timeout=60,
        )
        return response.json().get("response", "").strip()
    except Exception:
        return None


def _openai_generate(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None


def _rule_based_summary(biomechanics: BiomechanicsResult) -> tuple[str, list[str]]:
    """Deterministic fallback when no LLM is available."""
    risk = biomechanics.risk_level
    n_alerts = len(biomechanics.alerts)

    if risk == "low":
        summary = "Movement patterns appear within safe ranges. No significant biomechanical risks detected."
        recs = ["Continue current exercise programme.", "Maintain regular mobility check-ins."]
    elif risk == "medium":
        summary = f"Moderate movement risk detected ({n_alerts} issue). Review technique with a qualified physiotherapist."
        recs = ["Reduce load or intensity until reviewed.", "Focus on form before increasing repetitions."]
    else:
        summary = f"High movement risk detected ({n_alerts} issues). Immediate technique review recommended."
        recs = [
            "Stop current exercise until assessed by a physiotherapist.",
            "Do not increase intensity.",
            "Schedule a clinical assessment.",
        ]

    return summary, recs


def generate_insights(
    biomechanics: BiomechanicsResult,
    transcript: str | None = None,
) -> tuple[str, list[str]]:
    """Returns (summary, recommendations)."""
    prompt = build_prompt(biomechanics, transcript)

    # Try LLM backends in order
    llm_response = None
    if settings.openai_api_key:
        llm_response = _openai_generate(prompt)
    if not llm_response:
        llm_response = _ollama_generate(prompt)

    if llm_response:
        lines = [l.strip() for l in llm_response.split("\n") if l.strip()]
        summary = lines[0] if lines else ""
        recs = [l.lstrip("•-123456789. ") for l in lines[1:] if l]
        return summary, recs[:5]

    return _rule_based_summary(biomechanics)
