import RiskBadge from "./RiskBadge";
import MetricCard from "./MetricCard";
import MemoryPanel from "./MemoryPanel";

const API = import.meta.env.VITE_API_URL ?? "";

export default function ResultsPanel({ result }) {
  const { biomechanics, ai_summary, recommendations, frames_processed, duration_sec, transcript, overall_risk, longitudinal_insights } = result;

  return (
    <div className="space-y-6">
      <MemoryPanel insights={longitudinal_insights} />

      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Analysis Results</h2>
        <div className="flex items-center gap-3">
          <RiskBadge level={overall_risk} />
          <div className="flex gap-2">
            <a
              href={`${API}/api/v1/report/${result.session_id}/pdf`}
              download
              className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-200 px-3 py-1.5 rounded-lg transition"
            >
              ⬇ PDF Report
            </a>
            <a
              href={`${API}/api/v1/report/${result.session_id}/fhir`}
              download
              className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-200 px-3 py-1.5 rounded-lg transition"
            >
              ⬇ FHIR Export
            </a>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="Frames" value={frames_processed} unit="analyzed" />
        <MetricCard label="Duration" value={duration_sec} unit="sec" />
        <MetricCard label="Knee Angle" value={biomechanics.knee_angle ?? "—"} unit="°" />
        <MetricCard label="Hip Angle" value={biomechanics.hip_angle ?? "—"} unit="°" />
      </div>

      {/* Alerts */}
      {biomechanics.alerts.length > 0 && (
        <div className="bg-red-950 border border-red-800 rounded-xl p-4 space-y-2">
          <h3 className="font-semibold text-red-300">⚠️ Biomechanical Alerts</h3>
          <ul className="space-y-1">
            {biomechanics.alerts.map((a, i) => (
              <li key={i} className="text-sm text-red-200">{a}</li>
            ))}
          </ul>
        </div>
      )}

      {/* AI Summary */}
      {ai_summary && (
        <div className="bg-blue-950 border border-blue-800 rounded-xl p-4">
          <h3 className="font-semibold text-blue-300 mb-2">🧠 Clinical Summary</h3>
          <p className="text-sm text-blue-100 leading-relaxed">{ai_summary}</p>
        </div>
      )}

      {/* Recommendations */}
      {recommendations?.length > 0 && (
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 space-y-2">
          <h3 className="font-semibold text-green-300">✅ Recommendations</h3>
          <ul className="list-disc list-inside space-y-1">
            {recommendations.map((r, i) => (
              <li key={i} className="text-sm text-gray-200">{r}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Transcript */}
      {transcript && (
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <h3 className="font-semibold text-gray-300 mb-2">🎤 Audio Transcript</h3>
          <p className="text-sm text-gray-400 italic">{transcript}</p>
        </div>
      )}
    </div>
  );
}
