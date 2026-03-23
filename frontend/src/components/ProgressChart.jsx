const RISK_COLOR = { low: "#22c55e", medium: "#eab308", high: "#ef4444" };
const W = 480;
const H = 160;
const PAD = { top: 16, right: 16, bottom: 32, left: 40 };

function scaleY(val, min, max) {
  const range = max - min || 1;
  return PAD.top + (H - PAD.top - PAD.bottom) * (1 - (val - min) / range);
}

function scaleX(i, n) {
  const usable = W - PAD.left - PAD.right;
  return PAD.left + (n <= 1 ? usable / 2 : (i / (n - 1)) * usable);
}

function buildPath(values, minV, maxV, n) {
  const points = values.map((v, i) => (v != null ? `${scaleX(i, n)},${scaleY(v, minV, maxV)}` : null));
  let d = "";
  points.forEach((p, i) => {
    if (!p) return;
    d += d === "" || points.slice(0, i).every((x) => x === null) ? `M${p}` : `L${p}`;
  });
  return d;
}

export default function ProgressChart({ kneeAngleTrend = [], hipAngleTrend = [], riskHistory = [] }) {
  const n = Math.max(kneeAngleTrend.length, hipAngleTrend.length, 1);
  const allVals = [...kneeAngleTrend, ...hipAngleTrend].filter((v) => v != null);
  const minV = allVals.length ? Math.min(...allVals) - 5 : 40;
  const maxV = allVals.length ? Math.max(...allVals) + 5 : 120;

  const kneePath = buildPath(kneeAngleTrend, minV, maxV, n);
  const hipPath = buildPath(hipAngleTrend, minV, maxV, n);

  // Y-axis labels
  const yLabels = [minV, Math.round((minV + maxV) / 2), maxV];

  return (
    <div>
      <div className="flex gap-4 mb-2 text-xs">
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-blue-400 inline-block" />Knee angle</span>
        <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-purple-400 inline-block" />Hip angle</span>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ maxHeight: 180 }}>
        {/* Grid lines */}
        {yLabels.map((v) => (
          <g key={v}>
            <line x1={PAD.left} x2={W - PAD.right} y1={scaleY(v, minV, maxV)} y2={scaleY(v, minV, maxV)}
              stroke="#374151" strokeWidth="1" strokeDasharray="4,4" />
            <text x={PAD.left - 4} y={scaleY(v, minV, maxV) + 4} textAnchor="end" fill="#6b7280" fontSize="10">{Math.round(v)}°</text>
          </g>
        ))}

        {/* X-axis session labels */}
        {Array.from({ length: n }).map((_, i) => (
          <text key={i} x={scaleX(i, n)} y={H - 2} textAnchor="middle" fill="#6b7280" fontSize="9">S{i + 1}</text>
        ))}

        {/* Risk dots on x-axis */}
        {riskHistory.map((r, i) => (
          <circle key={i} cx={scaleX(i, n)} cy={H - 14} r={4} fill={RISK_COLOR[r] || "#6b7280"} />
        ))}

        {/* Lines */}
        {kneePath && <path d={kneePath} fill="none" stroke="#60a5fa" strokeWidth="2" strokeLinejoin="round" />}
        {hipPath && <path d={hipPath} fill="none" stroke="#c084fc" strokeWidth="2" strokeLinejoin="round" />}

        {/* Data points */}
        {kneeAngleTrend.map((v, i) => v != null && (
          <circle key={i} cx={scaleX(i, n)} cy={scaleY(v, minV, maxV)} r={3} fill="#60a5fa" />
        ))}
        {hipAngleTrend.map((v, i) => v != null && (
          <circle key={i} cx={scaleX(i, n)} cy={scaleY(v, minV, maxV)} r={3} fill="#c084fc" />
        ))}
      </svg>
      {/* Risk legend */}
      <div className="flex gap-3 mt-1 text-xs text-gray-500">
        <span>Risk dots:</span>
        {Object.entries(RISK_COLOR).map(([k, v]) => (
          <span key={k} className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full inline-block" style={{ background: v }} />{k}
          </span>
        ))}
      </div>
    </div>
  );
}
