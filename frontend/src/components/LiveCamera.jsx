import { useState, useRef, useEffect, useCallback } from "react";

const WS_URL = (() => {
  const base = import.meta.env.VITE_API_URL || "";
  if (base.startsWith("http")) return base.replace(/^http/, "ws") + "/api/v1/live";
  return `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/api/v1/live`;
})();

export default function LiveCamera({ exerciseType = "general" }) {
  const [active, setActive] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  const stop = useCallback(() => {
    clearInterval(intervalRef.current);
    if (wsRef.current) wsRef.current.close();
    if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
    setActive(false);
    setMetrics(null);
  }, []);

  const start = useCallback(async () => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onmessage = (e) => {
        try { setMetrics(JSON.parse(e.data)); } catch {}
      };
      ws.onerror = () => setError("WebSocket connection failed. Ensure backend supports live mode.");
      ws.onopen = () => {
        setActive(true);
        intervalRef.current = setInterval(() => {
          if (ws.readyState !== WebSocket.OPEN) return;
          const video = videoRef.current;
          const canvas = canvasRef.current;
          if (!video || !canvas) return;
          canvas.width = 320;
          canvas.height = 240;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(video, 0, 0, 320, 240);
          const b64 = canvas.toDataURL("image/jpeg", 0.6).split(",")[1];
          ws.send(JSON.stringify({ frame: b64, exercise_type: exerciseType }));
        }, 800);
      };
    } catch (err) {
      setError(err.message.includes("Permission") ? "Camera permission denied." : err.message);
    }
  }, [exerciseType]);

  useEffect(() => () => stop(), [stop]);

  const riskColor = { low: "text-green-400", medium: "text-yellow-400", high: "text-red-400" };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">📷 Live Camera Analysis</h2>
        {active && <span className="flex items-center gap-2 text-sm text-green-400"><span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />Live</span>}
      </div>

      <div className="relative bg-black rounded-xl overflow-hidden aspect-video max-h-72 flex items-center justify-center">
        <video ref={videoRef} className="w-full h-full object-cover" muted playsInline />
        <canvas ref={canvasRef} className="hidden" />
        {!active && (
          <div className="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">
            Camera preview will appear here
          </div>
        )}
      </div>

      {error && <p className="text-red-400 text-sm">{error}</p>}

      <div className="flex gap-3">
        {!active ? (
          <button onClick={start} className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-xl transition">
            Start Camera
          </button>
        ) : (
          <button onClick={stop} className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-xl transition">
            Stop
          </button>
        )}
      </div>

      {metrics && (
        <div className="space-y-3">
          {!metrics.pose_detected && (
            <p className="text-yellow-400 text-sm">⚠️ No pose detected — ensure full body is visible</p>
          )}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-gray-800 rounded-xl p-3 text-center">
              <div className="text-2xl font-bold text-blue-300">{metrics.knee_angle?.toFixed(1) ?? "—"}°</div>
              <div className="text-xs text-gray-400 mt-1">Knee Angle</div>
            </div>
            <div className="bg-gray-800 rounded-xl p-3 text-center">
              <div className="text-2xl font-bold text-purple-300">{metrics.hip_angle?.toFixed(1) ?? "—"}°</div>
              <div className="text-xs text-gray-400 mt-1">Hip Angle</div>
            </div>
            <div className="bg-gray-800 rounded-xl p-3 text-center">
              <div className={`text-2xl font-bold uppercase ${riskColor[metrics.risk_level] || "text-gray-300"}`}>
                {metrics.risk_level}
              </div>
              <div className="text-xs text-gray-400 mt-1">Risk</div>
            </div>
          </div>
          {metrics.alerts?.length > 0 && (
            <div className="bg-red-950 border border-red-800 rounded-xl p-3 space-y-1">
              {metrics.alerts.map((a, i) => <p key={i} className="text-red-200 text-sm">{a}</p>)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
