"""Exercise library with clinical biomechanical thresholds per movement."""
from typing import Optional

EXERCISES = {
    "general": {
        "name": "General Movement",
        "thresholds": {"knee_min": 70, "hip_min": 60, "spine_dev_max": 0.08, "asym_max": 0.05},
        "cues": ["Maintain neutral spine", "Keep knees aligned with toes", "Engage core throughout"],
    },
    "squat": {
        "name": "Squat",
        "thresholds": {"knee_min": 60, "hip_min": 55, "spine_dev_max": 0.06, "asym_max": 0.04},
        "cues": ["Chest up, spine neutral", "Knees track over toes", "Hip crease below knee at bottom", "Weight through heels"],
    },
    "deadlift": {
        "name": "Deadlift",
        "thresholds": {"knee_min": 90, "hip_min": 45, "spine_dev_max": 0.05, "asym_max": 0.03},
        "cues": ["Neutral spine throughout — no rounding", "Bar close to body", "Drive hips forward at lockout", "Shoulders packed, lats engaged"],
    },
    "shoulder_press": {
        "name": "Shoulder Press",
        "thresholds": {"knee_min": 150, "hip_min": 150, "spine_dev_max": 0.05, "asym_max": 0.04},
        "cues": ["Core braced, no lumbar hyperextension", "Elbows slightly forward at start", "Full overhead lockout", "Wrists stacked over elbows"],
    },
    "lunge": {
        "name": "Lunge",
        "thresholds": {"knee_min": 65, "hip_min": 50, "spine_dev_max": 0.07, "asym_max": 0.06},
        "cues": ["Front knee tracks over second toe", "Torso upright", "Back knee hovers above floor", "Equal weight distribution"],
    },
    "hip_hinge": {
        "name": "Hip Hinge / RDL",
        "thresholds": {"knee_min": 140, "hip_min": 40, "spine_dev_max": 0.04, "asym_max": 0.03},
        "cues": ["Hinge at hips, not waist", "Soft knee bend throughout", "Spine neutral, chest proud", "Push hips back to initiate"],
    },
}


def get_exercise(exercise_type: str) -> dict:
    return EXERCISES.get(exercise_type, EXERCISES["general"])


def list_exercises() -> list:
    return [{"id": k, "name": v["name"], "cues": v["cues"]} for k, v in EXERCISES.items()]
