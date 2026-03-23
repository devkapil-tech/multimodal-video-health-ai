import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import Header from "./components/Header";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        <UploadPanel onResult={setResult} onLoading={setLoading} />
        {loading && (
          <div className="text-center text-blue-400 animate-pulse text-lg">
            Analysing movement — extracting poses, biomechanics, and insights...
          </div>
        )}
        {result && <ResultsPanel result={result} />}
      </main>
    </div>
  );
}
