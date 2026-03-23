import ProgressChart from "./ProgressChart";

const TREND_CONFIG = {
  improving: { color: "text-green-400", bg: "bg-green-950 border-green-800", icon: "📈", label: "Improving" },
  worsening: { color: "text-red-400", bg: "bg-red-950 border-red-800", icon: "📉", label: "Worsening" },
  stable: { color: "text-yellow-400", bg: "bg-yellow-950 border-yellow-800", icon: "➡️", label: "Stable" },
  insufficient_data: { color: "text-gray-400", bg: "bg-gray-900 border-gray-700", icon: "📊", label: "Tracking..." },
};

export default function MemoryPanel({ insights }) {
  if (!insights) return null;

  const cfg = TREND_CONFIG[insights.trend] || TREND_CONFIG.insufficient_data;

  return (
    <div className={`border rounded-2xl p-5 space-y-4 ${cfg.bg}`}>
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-lg">🧠 Longitudinal Memory</h3>
        <div className={`flex items-center gap-2 text-sm font-semibold ${cfg.color}`}>
          <span>{cfg.icon}</span>
          <span>{cfg.label}</span>
          <span className="text-gray-400 font-normal">({insights.session_count} sessions)</span>
        </div>
      </div>

      {insights.key_observation && (
        <div className="bg-black/20 rounded-xl p-3">
          <p className="text-sm font-medium">{insights.key_observation}</p>
        </div>
      )}

      {insights.trend_summary && (
        <p className="text-sm text-gray-300">{insights.trend_summary}</p>
      )}

      {insights.session_count >= 2 && (
        <div className="bg-black/20 rounded-xl p-4">
          <p className="text-xs text-gray-400 mb-3 font-semibold uppercase tracking-wide">Progress Chart</p>
          <ProgressChart
            kneeAngleTrend={insights.knee_angle_trend}
            hipAngleTrend={insights.hip_angle_trend}
            riskHistory={insights.risk_history}
          />
        </div>
      )}

      {insights.session_count === 1 && (
        <p className="text-xs text-gray-500">Upload another session with the same token to see progress trends.</p>
      )}
    </div>
  );
}
