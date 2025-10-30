import React, { useState } from "react";

const RecommendPage: React.FC = () => {
  const [graph, setGraph] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const userId = "user123"; // can be dynamic later

  const fetchGraph = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`http://127.0.0.1:8000/recommend/graph/${userId}`);
      if (!res.ok) throw new Error("Failed to fetch graph");
      const data = await res.json();
      setGraph(data.graph);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-300 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-8 drop-shadow">
        🧠 Your Recommendation Graph
      </h1>

      <button
        onClick={fetchGraph}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-xl shadow-lg transition-transform transform hover:scale-105"
      >
        {loading ? "Generating Graph..." : "Show Graph"}
      </button>

      {error && (
        <p className="text-red-500 font-medium mt-4">
          ❌ {error}
        </p>
      )}

      {graph && (
        <div className="mt-8 flex flex-col items-center">
          <img
            src={graph}
            alt="Recommendation Graph"
            className="border-4 border-white rounded-2xl shadow-xl w-[80%] max-w-3xl"
          />
          <p className="mt-4 text-gray-600 text-sm">
            🟢 Liked Products | 🔴 Recommended Products | ⚪ Other Products
          </p>
        </div>
      )}
    </div>
  );
};

export default RecommendPage;
