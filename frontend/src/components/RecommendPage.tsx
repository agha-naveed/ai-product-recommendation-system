import React, { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  _id: string;
  title: string;
  price: number;
  rating: number;
  category: string;
  image: string;
}

const RecommendPage: React.FC = () => {
  const [recs, setRecs] = useState<Product[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/recommend/user123").then(res => setRecs(res.data.recommendations));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">🎯 Your Personalized Recommendations</h1>
      {recs.length === 0 ? (
        <p>No recommendations yet. Try liking a few products!</p>
      ) : (
        <div className="grid grid-cols-4 gap-6">
          {recs.map(p => (
            <div key={p._id} className="border rounded-xl shadow-md p-3 hover:shadow-lg transition">
              <img src={p.image} alt={p.title} className="h-48 w-full object-cover rounded-lg" />
              <h3 className="text-lg font-semibold mt-2">{p.title}</h3>
              <p className="text-sm text-gray-500">{p.category}</p>
              <p className="font-bold">${p.price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecommendPage;
