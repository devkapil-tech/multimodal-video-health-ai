export default function MetricCard({ label, value, unit }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-xs text-gray-500">{unit}</p>
    </div>
  );
}
