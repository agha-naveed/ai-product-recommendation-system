// frontend/src/pages/RecommendationsPage.tsx
import React, { useEffect, useState } from "react";

interface Product {
  id?: number;
  title?: string;
  name?: string;
  price?: number;
  image?: string;
  images?: string[];
  category?: string | { name: string };
  rating?: number | { rate: number };
}

const RecommendationsPage: React.FC = () => {
  const [recs, setRecs] = useState<Product[]>([]);

  useEffect(() => {
    const data = localStorage.getItem("recommendations");
    if (data) {
      try {
        const parsed: Product[] = JSON.parse(data);
        setRecs(parsed);
      } catch (err) {
        console.error("Error parsing recommendations:", err);
      }
    }
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Recommended Products</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {recs.map((p, idx) => (
          <div
            key={p.id ?? idx}
            className="border p-2 rounded shadow-md hover:shadow-lg transition-shadow duration-200"
          >
            <img
              src={p.image || p.images?.[0]}
              alt={p.title || p.name || "Product"}
              className="w-full h-40 object-cover rounded"
            />
            <h2 className="text-lg font-semibold mt-2">
              {p.title || p.name || "Untitled"}
            </h2>
            <p className="text-gray-600">${p.price?.toFixed(2) ?? "N/A"}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationsPage;
