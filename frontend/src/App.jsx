import { useState } from "react";
import Header from "./components/Header";
import UploadPanel from "./components/UploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import LiveCamera from "./components/LiveCamera";
import ComparisonPanel from "./components/ComparisonPanel";
import ExerciseSelector from "./components/ExerciseSelector";
import PatientTokenInput from "./components/PatientTokenInput";

const TABS = [
  { id: "upload", label: "📤 Upload Video" },
  { id: "live", label: "📷 Live Camera" },
  { id: "compare", label: "📊 Compare" },
];

export default function App() {
  const [tab, setTab] = useState("upload");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [exerciseType, setExerciseType] = useState("general");
  const [patientToken, setPatientToken] = useState("");

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-10 space-y-6">
        {/* Patient token — enables longitudinal memory */}
        <PatientTokenInput value={patientToken} onChange={setPatientToken} />

        {/* Exercise selector — applies to all modes */}
        <ExerciseSelector value={exerciseType} onChange={setExerciseType} />

        {/* Tab bar */}
        <div className="flex gap-2 border-b border-gray-800 pb-0">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => { setTab(t.id); setResult(null); }}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg transition border-b-2 -mb-px ${
                tab === t.id
                  ? "border-blue-500 text-blue-400 bg-gray-900"
                  : "border-transparent text-gray-400 hover:text-gray-200"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {tab === "upload" && (
          <div className="space-y-6">
            <UploadPanel onResult={setResult} onLoading={setLoading} exerciseType={exerciseType} patientToken={patientToken} />
            {loading && (
              <div className="text-center text-blue-400 animate-pulse text-lg">
                Analysing movement — extracting poses, biomechanics, and insights...
              </div>
            )}
            {result && <ResultsPanel result={result} />}
          </div>
        )}

        {tab === "live" && <LiveCamera exerciseType={exerciseType} />}
        {tab === "compare" && <ComparisonPanel exerciseType={exerciseType} />}
      </main>
    </div>
  );
}
