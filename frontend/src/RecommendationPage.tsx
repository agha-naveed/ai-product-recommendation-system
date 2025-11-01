import React, { useEffect, useState } from "react";

interface Product {
  id?: number;
  title?: string;
  name?: string;
  price?: number;
  image?: string;
  rating?: number;
  images?: string[];
  category?: string;
}

const RecommendationsPage: React.FC = () => {
  const [recs, setRecs] = useState<Product[]>([]);

  useEffect(() => {
    const data = localStorage.getItem("recommendations");
    if (data) setRecs(JSON.parse(data));
  }, []);

  return (
    <div className="min-h-screen from-indigo-50 to-purple-100 p-8">
      <h1 className="text-4xl font-bold text-center text-gray-800 mb-10">
        🌟 Your AI-Powered Recommendations
      </h1>

      <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {recs.map((p, i) => (
          <div
            key={"new-"+i}
            className="bg-white rounded-2xl shadow-lg hover:shadow-2xl overflow-hidden transform transition hover:-translate-y-1"
          >
            <img
              src={p.image || p.images?.[0]}
              alt={p.title || p.name}
              className="w-full h-56 object-cover"
            />
            <div className="p-4 text-center">
              <h2 className="text-lg font-semibold text-gray-800 truncate">
                {p.title || p.name}
              </h2>
              <p className="text-gray-600 flex items-center justify-center">
                rating: {p.rating}
              </p>
              <p className="text-indigo-600 text-xl font-bold">
                ${p.price?.toFixed(2)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationsPage;
