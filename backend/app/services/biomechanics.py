"""
Biomechanics Engine — the clinical differentiation layer.
Converts raw pose landmarks into actionable health insights.
"""
import math
from typing import List
from app.schemas.analysis import FramePose, BiomechanicsResult


def angle_between(a: tuple, b: tuple, c: tuple) -> float:
    """Calculate angle at point b formed by a-b-c."""
    v1 = (a[0] - b[0], a[1] - b[1])
    v2 = (c[0] - b[0], c[1] - b[1])
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    if mag1 * mag2 == 0:
        return 0.0
    cos_angle = max(-1, min(1, dot / (mag1 * mag2)))
    return math.degrees(math.acos(cos_angle))


def lateral_deviation(shoulder: tuple, hip: tuple) -> float:
    """Measure lateral spine deviation (x-axis lean)."""
    return abs(shoulder[0] - hip[0])


def asymmetry_score(landmarks: dict) -> float:
    """Compare left vs right side height difference."""
    if not landmarks:
        return 0.0
    ls = landmarks.get("left_shoulder", (0, 0))
    rs = landmarks.get("right_shoulder", (0, 0))
    lh = landmarks.get("left_hip", (0, 0))
    rh = landmarks.get("right_hip", (0, 0))
    shoulder_diff = abs(ls[1] - rs[1])
    hip_diff = abs(lh[1] - rh[1])
    return round((shoulder_diff + hip_diff) / 2, 4)


def analyze_biomechanics(pose_results: List[FramePose]) -> BiomechanicsResult:
    valid = [p for p in pose_results if p.shoulder and p.hip and p.knee and p.ankle]
    alerts = []
    knee_angles, hip_angles, deviations, asym_scores = [], [], [], []

    for pose in valid:
        # Knee flexion angle
        k_angle = angle_between(pose.hip, pose.knee, pose.ankle)
        knee_angles.append(k_angle)

        # Hip flexion angle
        h_angle = angle_between(pose.shoulder, pose.hip, pose.knee)
        hip_angles.append(h_angle)

        # Spine deviation
        dev = lateral_deviation(pose.shoulder, pose.hip)
        deviations.append(dev)

        # Asymmetry
        if pose.landmarks:
            asym_scores.append(asymmetry_score(pose.landmarks))

    # --- Clinical thresholds ---
    avg_knee = sum(knee_angles) / len(knee_angles) if knee_angles else None
    avg_hip = sum(hip_angles) / len(hip_angles) if hip_angles else None
    avg_dev = sum(deviations) / len(deviations) if deviations else None
    avg_asym = sum(asym_scores) / len(asym_scores) if asym_scores else None

    if avg_knee is not None and avg_knee < 70:
        alerts.append(f"⚠️ Deep knee flexion detected (avg {avg_knee:.1f}°) — increased knee joint stress")
    if avg_hip is not None and avg_hip < 60:
        alerts.append(f"⚠️ Excessive hip flexion (avg {avg_hip:.1f}°) — lumbar load risk")
    if avg_dev is not None and avg_dev > 0.08:
        alerts.append(f"⚠️ Lateral spine deviation detected ({avg_dev:.3f}) — possible scoliosis compensation")
    if avg_asym is not None and avg_asym > 0.05:
        alerts.append(f"⚠️ Bilateral asymmetry detected ({avg_asym:.3f}) — uneven muscle loading")

    # Overall risk level
    risk_level = "low"
    if len(alerts) == 1:
        risk_level = "medium"
    elif len(alerts) >= 2:
        risk_level = "high"

    return BiomechanicsResult(
        knee_angle=round(avg_knee, 2) if avg_knee else None,
        hip_angle=round(avg_hip, 2) if avg_hip else None,
        spine_deviation=round(avg_dev, 4) if avg_dev else None,
        asymmetry_score=round(avg_asym, 4) if avg_asym else None,
        alerts=alerts,
        risk_level=risk_level,
    )
