export default function Header() {
  return (
    <header className="border-b border-gray-800 bg-gray-900 px-6 py-4">
      <div className="max-w-5xl mx-auto flex items-center gap-3">
        <span className="text-2xl">🏥</span>
        <div>
          <h1 className="text-xl font-bold text-white">Multimodal Video Health AI</h1>
          <p className="text-xs text-gray-400">Movement analysis · Posture detection · Clinical insights</p>
        </div>
        <span className="ml-auto text-xs bg-green-900 text-green-300 px-2 py-1 rounded-full">
          Open Source
        </span>
      </div>
    </header>
  );
}
