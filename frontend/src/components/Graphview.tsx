import React, { useState } from "react";

const GraphView = () => {
  const [graph, setGraph] = useState<string | null>(null);

  const fetchGraph = async () => {
    const res = await fetch(`http://127.0.0.1:8000/recommend/graph/user123`);
    const data = await res.json();
    setGraph(data.graph);
  };

  return (
    <div className="flex flex-col items-center">
      <button
        onClick={fetchGraph}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-600 mt-4"
      >
        Show Recommendation Graph
      </button>

      {graph && (
        <img
          src={graph}
          alt="Recommendation Graph"
          className="mt-6 border rounded-xl shadow-lg w-3/4"
        />
      )}
    </div>
  );
};

export default GraphView;