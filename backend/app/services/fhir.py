"""FHIR R4 DiagnosticReport builder for movement analysis results."""
from datetime import datetime, timezone
from typing import Any, Dict
from app.schemas.analysis import AnalysisResult


def build_fhir_report(result: AnalysisResult) -> Dict[str, Any]:
    """Return a FHIR R4 Bundle containing DiagnosticReport + Observations."""
    now = datetime.now(timezone.utc).isoformat()
    bm = result.biomechanics

    def observation(code: str, display: str, value: Any, unit: str) -> dict:
        return {
            "resourceType": "Observation",
            "id": f"obs-{code.lower().replace(' ', '-')}",
            "status": "final",
            "code": {
                "coding": [{"system": "http://loinc.org", "code": code, "display": display}],
                "text": display,
            },
            "valueQuantity": {"value": value, "unit": unit, "system": "http://unitsofmeasure.org"},
            "effectiveDateTime": now,
        }

    observations = []
    if bm.knee_angle is not None:
        observations.append(observation("8361-8", "Knee flexion angle", bm.knee_angle, "deg"))
    if bm.hip_angle is not None:
        observations.append(observation("8360-0", "Hip flexion angle", bm.hip_angle, "deg"))
    if bm.spine_deviation is not None:
        observations.append(observation("59408-5", "Lateral spine deviation", round(bm.spine_deviation, 4), "{ratio}"))
    if bm.asymmetry_score is not None:
        observations.append(observation("72514-3", "Bilateral asymmetry score", round(bm.asymmetry_score, 4), "{ratio}"))

    risk_map = {"low": "LA6750-9", "medium": "LA6751-7", "high": "LA6752-5"}

    diagnostic_report = {
        "resourceType": "DiagnosticReport",
        "id": result.session_id,
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                        "code": "PT",
                        "display": "Physical Therapy",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "80394-3",
                    "display": "Physical therapy movement analysis",
                }
            ],
            "text": f"Movement Analysis — {result.exercise_type.title()}",
        },
        "effectiveDateTime": now,
        "issued": now,
        "result": [{"reference": f"#obs-{obs['id']}"} for obs in observations],
        "conclusion": result.ai_summary or f"Overall risk: {result.overall_risk}",
        "conclusionCode": [
            {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": risk_map.get(result.overall_risk, "LA6750-9"),
                        "display": f"Risk level: {result.overall_risk}",
                    }
                ]
            }
        ],
        "extension": [
            {
                "url": "https://github.com/devkapil-tech/multimodal-video-health-ai",
                "valueString": f"session_id={result.session_id}, exercise={result.exercise_type}, frames={result.frames_processed}",
            }
        ],
    }

    return {
        "resourceType": "Bundle",
        "id": f"bundle-{result.session_id}",
        "type": "collection",
        "timestamp": now,
        "entry": [
            {"resource": diagnostic_report},
            *[{"resource": obs} for obs in observations],
        ],
    }
