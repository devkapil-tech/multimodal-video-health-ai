import { useRef, useState } from "react";
import useSWRMutation from "swr/mutation";
import RiskBadge from "./RiskBadge";

const API = import.meta.env.VITE_API_URL ?? "";

async function compareVideos(url, { arg: { before, after, exerciseType } }) {
  const fd = new FormData();
  fd.append("before", before);
  fd.append("after", after);
  fd.append("exercise_type", exerciseType);
  const res = await fetch(url, { method: "POST", body: fd });
  if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || "Comparison failed");
  return res.json();
}

function DeltaBadge({ delta, unit = "", invertGood = false }) {
  if (delta === null || delta === undefined) return <span className="text-gray-500 text-xs">—</span>;
  const improved = invertGood ? delta < 0 : delta > 0;
  return (
    <span className={`text-xs font-semibold ${improved ? "text-green-400" : delta === 0 ? "text-gray-400" : "text-red-400"}`}>
      {delta > 0 ? "+" : ""}{delta}{unit}
    </span>
  );
}

function VideoSlot({ label, file, onChange, inputRef }) {
  return (
    <div className="flex-1">
      <p className="text-sm font-semibold text-gray-300 mb-2">{label}</p>
      <div
        className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 transition"
        onClick={() => inputRef.current.click()}
      >
        {file ? (
          <p className="text-blue-400 text-sm">✅ {file.name}</p>
        ) : (
          <p className="text-gray-500 text-sm">Click to select video</p>
        )}
        <input ref={inputRef} type="file" accept="video/*" className="hidden" onChange={(e) => onChange(e.target.files[0])} />
      </div>
    </div>
  );
}

function ResultColumn({ label, result, color }) {
  const bm = result.biomechanics;
  return (
    <div className={`flex-1 bg-gray-900 border ${color} rounded-xl p-4 space-y-3`}>
      <div className="flex items-center justify-between">
        <h4 className="font-semibold">{label}</h4>
        <RiskBadge level={result.overall_risk} />
      </div>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between"><span className="text-gray-400">Knee Angle</span><span>{bm.knee_angle ?? "—"}°</span></div>
        <div className="flex justify-between"><span className="text-gray-400">Hip Angle</span><span>{bm.hip_angle ?? "—"}°</span></div>
        <div className="flex justify-between"><span className="text-gray-400">Spine Dev.</span><span>{bm.spine_deviation ?? "—"}</span></div>
        <div className="flex justify-between"><span className="text-gray-400">Asymmetry</span><span>{bm.asymmetry_score ?? "—"}</span></div>
        <div className="flex justify-between"><span className="text-gray-400">Frames</span><span>{result.frames_processed}</span></div>
      </div>
      {bm.alerts.length > 0 && (
        <div className="text-xs text-red-300 space-y-1">
          {bm.alerts.map((a, i) => <p key={i}>{a}</p>)}
        </div>
      )}
    </div>
  );
}

export default function ComparisonPanel({ exerciseType = "general" }) {
  const [before, setBefore] = useState(null);
  const [after, setAfter] = useState(null);
  const beforeRef = useRef();
  const afterRef = useRef();

  const { trigger, isMutating, data, error } = useSWRMutation(
    `${API}/api/v1/compare`,
    compareVideos
  );

  const handleCompare = () => {
    if (!before || !after) return;
    trigger({ before, after, exerciseType });
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 space-y-5">
      <h2 className="text-lg font-semibold">📊 Before / After Comparison</h2>

      <div className="flex gap-4">
        <VideoSlot label="Before" file={before} onChange={setBefore} inputRef={beforeRef} />
        <VideoSlot label="After" file={after} onChange={setAfter} inputRef={afterRef} />
      </div>

      {error && <p className="text-red-400 text-sm">{error.message}</p>}

      <button
        onClick={handleCompare}
        disabled={!before || !after || isMutating}
        className="w-full bg-purple-600 hover:bg-purple-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition"
      >
        {isMutating ? "Comparing..." : "Compare Videos"}
      </button>

      {data && (
        <div className="space-y-4">
          <div className="flex gap-4">
            <ResultColumn label="Before" result={data.before} color="border-gray-700" />
            <ResultColumn label="After" result={data.after} color="border-blue-700" />
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-xl p-4">
            <h4 className="font-semibold text-sm mb-3">📈 Improvement Delta</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="flex justify-between"><span className="text-gray-400">Knee Angle</span><DeltaBadge delta={data.delta.knee_angle} unit="°" /></div>
              <div className="flex justify-between"><span className="text-gray-400">Hip Angle</span><DeltaBadge delta={data.delta.hip_angle} unit="°" /></div>
              <div className="flex justify-between"><span className="text-gray-400">Spine Dev.</span><DeltaBadge delta={data.delta.spine_deviation} invertGood /></div>
              <div className="flex justify-between"><span className="text-gray-400">Asymmetry</span><DeltaBadge delta={data.delta.asymmetry_score} invertGood /></div>
            </div>
            {data.delta.risk_improved && (
              <p className="text-green-400 text-sm mt-3 font-semibold">✅ Risk level improved!</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
