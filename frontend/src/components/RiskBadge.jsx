const styles = {
  low:    "bg-green-900 text-green-300 border-green-700",
  medium: "bg-yellow-900 text-yellow-300 border-yellow-700",
  high:   "bg-red-900 text-red-300 border-red-700",
};

const labels = { low: "✅ Low Risk", medium: "⚠️ Medium Risk", high: "🚨 High Risk" };

export default function RiskBadge({ level }) {
  return (
    <span className={`border px-3 py-1 rounded-full text-sm font-semibold ${styles[level] ?? styles.low}`}>
      {labels[level] ?? level}
    </span>
  );
}
