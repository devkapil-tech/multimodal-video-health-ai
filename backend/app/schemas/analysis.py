from pydantic import BaseModel
from typing import List, Optional


class PoseLandmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: float


class FramePose(BaseModel):
    frame_index: int
    timestamp_sec: float
    landmarks: Optional[dict]
    shoulder: Optional[tuple]
    hip: Optional[tuple]
    knee: Optional[tuple]
    ankle: Optional[tuple]


class BiomechanicsResult(BaseModel):
    knee_angle: Optional[float]
    hip_angle: Optional[float]
    spine_deviation: Optional[float]
    asymmetry_score: Optional[float]
    alerts: List[str]
    risk_level: str  # low / medium / high


class LongitudinalInsights(BaseModel):
    session_count: int
    trend: str  # improving | worsening | stable | insufficient_data
    trend_summary: str
    knee_angle_trend: List[Optional[float]]
    hip_angle_trend: List[Optional[float]]
    risk_history: List[str]
    key_observation: Optional[str] = None


class SessionSummary(BaseModel):
    session_id: str
    exercise_type: str
    knee_angle: Optional[float]
    hip_angle: Optional[float]
    risk_level: str
    created_at: Optional[str] = None


class AnalysisResult(BaseModel):
    session_id: str
    frames_processed: int
    duration_sec: float
    pose_results: List[FramePose]
    biomechanics: BiomechanicsResult
    transcript: Optional[str]
    ai_summary: Optional[str]
    recommendations: List[str]
    overall_risk: str
    exercise_type: str = "general"
    patient_token: Optional[str] = None
    longitudinal_insights: Optional[LongitudinalInsights] = None
