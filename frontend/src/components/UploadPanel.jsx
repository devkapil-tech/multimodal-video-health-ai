import { useState, useRef } from "react";
import useSWRMutation from "swr/mutation";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function uploadVideo(url, { arg: file }) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(url, { method: "POST", body: formData });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Upload failed (${res.status})`);
  }
  return res.json();
}

export default function UploadPanel({ onResult, onLoading }) {
  const [file, setFile] = useState(null);
  const inputRef = useRef();

  const { trigger, isMutating, error } = useSWRMutation(
    `${API}/api/v1/upload`,
    uploadVideo,
    {
      onSuccess(data) {
        onResult(data);
        onLoading(false);
      },
      onError() {
        onLoading(false);
      },
    }
  );

  const handleUpload = () => {
    if (!file) return;
    onLoading(true);
    onResult(null);
    trigger(file);
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 space-y-4">
      <h2 className="text-lg font-semibold">Upload Movement Video</h2>
      <p className="text-sm text-gray-400">
        Supported: MP4, MOV, AVI, MKV, WebM · Max 500 MB
      </p>

      <div
        className="border-2 border-dashed border-gray-700 rounded-xl p-8 text-center cursor-pointer hover:border-blue-500 transition"
        onClick={() => inputRef.current.click()}
      >
        {file ? (
          <p className="text-blue-400">✅ {file.name} ({(file.size / 1e6).toFixed(1)} MB)</p>
        ) : (
          <p className="text-gray-500">Click to select or drag a video here</p>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="video/*"
          className="hidden"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      {error && <p className="text-red-400 text-sm">{error.message}</p>}

      <button
        onClick={handleUpload}
        disabled={!file || isMutating}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition"
      >
        {isMutating ? "Analysing..." : "Analyse Video"}
      </button>
    </div>
  );
}
