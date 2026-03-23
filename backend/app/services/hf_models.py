"""Optional HuggingFace Inference API enrichment layer."""
import os
import logging
from typing import Optional, Tuple
from app.schemas.analysis import BiomechanicsResult

logger = logging.getLogger(__name__)

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")


def hf_enrich_summary(
    biomechanics: BiomechanicsResult,
    exercise_type: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[str], list]:
    """
    Use HuggingFace Inference API to generate clinical summary.
    Returns (summary, recommendations) or (None, []) if unavailable.
    """
    if not HF_TOKEN:
        return None, []

    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)

        prompt = f"""You are a physiotherapy AI assistant. Analyze this movement assessment:

Exercise: {exercise_type}
Knee angle: {biomechanics.knee_angle}°
Hip angle: {biomechanics.hip_angle}°
Spine deviation: {biomechanics.spine_deviation}
Asymmetry score: {biomechanics.asymmetry_score}
Risk level: {biomechanics.risk_level}
Alerts: {'; '.join(biomechanics.alerts) if biomechanics.alerts else 'None'}
{f'Patient description: {transcript}' if transcript else ''}

Provide:
1. A 2-sentence clinical summary
2. Three specific corrective recommendations

Format: SUMMARY: <text> | RECOMMENDATIONS: <rec1> | <rec2> | <rec3>"""

        response = client.text_generation(prompt, max_new_tokens=300, temperature=0.3)
        text = response.strip()

        summary = None
        recs = []
        if "SUMMARY:" in text and "RECOMMENDATIONS:" in text:
            parts = text.split("RECOMMENDATIONS:")
            summary = parts[0].replace("SUMMARY:", "").strip()
            recs = [r.strip() for r in parts[1].split("|") if r.strip()]

        return summary, recs

    except Exception as e:
        logger.warning(f"HuggingFace enrichment failed: {e}")
        return None, []
