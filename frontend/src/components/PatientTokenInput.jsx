import { useState, useEffect } from "react";

const STORAGE_KEY = "mvha_patient_token";

export default function PatientTokenInput({ value, onChange }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && !value) onChange(saved);
  }, []);

  const save = () => {
    const trimmed = draft.trim();
    onChange(trimmed);
    if (trimmed) localStorage.setItem(STORAGE_KEY, trimmed);
    else localStorage.removeItem(STORAGE_KEY);
    setEditing(false);
  };

  const clear = () => {
    onChange("");
    setDraft("");
    localStorage.removeItem(STORAGE_KEY);
    setEditing(false);
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <div>
          <span className="text-sm font-semibold text-gray-200">🧠 Patient Token</span>
          <span className="ml-2 text-xs text-gray-500">Enables longitudinal memory across sessions</span>
        </div>
        {!editing && (
          <button onClick={() => { setDraft(value); setEditing(true); }}
            className="text-xs text-blue-400 hover:text-blue-300 transition">
            {value ? "Change" : "Set token"}
          </button>
        )}
      </div>

      {editing ? (
        <div className="flex gap-2">
          <input
            type="text"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") save(); if (e.key === "Escape") setEditing(false); }}
            placeholder="e.g. john-knee-rehab-2026"
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            autoFocus
          />
          <button onClick={save} className="bg-blue-600 hover:bg-blue-700 text-white text-xs px-3 py-1.5 rounded-lg transition">Save</button>
          <button onClick={clear} className="bg-gray-700 hover:bg-gray-600 text-white text-xs px-3 py-1.5 rounded-lg transition">Clear</button>
        </div>
      ) : (
        <div className="flex items-center gap-2">
          {value ? (
            <>
              <span className="text-sm font-mono bg-gray-800 px-2 py-1 rounded text-green-300">{value}</span>
              <span className="text-xs text-green-500">● Memory active</span>
            </>
          ) : (
            <span className="text-xs text-gray-500">No token set — sessions won't be remembered</span>
          )}
        </div>
      )}
      <p className="text-xs text-gray-600 mt-2">No personal data stored. Token is a private identifier you create.</p>
    </div>
  );
}
