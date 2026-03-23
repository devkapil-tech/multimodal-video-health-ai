const EXERCISES = [
  { id: "general", emoji: "🏃", name: "General Movement", desc: "Any movement pattern" },
  { id: "squat", emoji: "🏋️", name: "Squat", desc: "Back / front / goblet squat" },
  { id: "deadlift", emoji: "⚡", name: "Deadlift", desc: "Conventional / sumo / RDL" },
  { id: "shoulder_press", emoji: "💪", name: "Shoulder Press", desc: "OHP / push press" },
  { id: "lunge", emoji: "🚶", name: "Lunge", desc: "Forward / reverse / lateral" },
  { id: "hip_hinge", emoji: "🔄", name: "Hip Hinge", desc: "RDL / good morning" },
];

export default function ExerciseSelector({ value, onChange }) {
  return (
    <div>
      <p className="text-sm text-gray-400 mb-3">Select exercise type for accurate thresholds</p>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {EXERCISES.map((ex) => (
          <button
            key={ex.id}
            onClick={() => onChange(ex.id)}
            className={`text-left p-3 rounded-xl border transition ${
              value === ex.id
                ? "border-blue-500 bg-blue-950 text-blue-100"
                : "border-gray-700 bg-gray-900 text-gray-300 hover:border-gray-500"
            }`}
          >
            <div className="text-2xl mb-1">{ex.emoji}</div>
            <div className="font-semibold text-sm">{ex.name}</div>
            <div className="text-xs text-gray-400">{ex.desc}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
