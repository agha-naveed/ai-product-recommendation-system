import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface Product {
  _id: string;
  title: string;
  price: number;
  rating: number;
  category: string;
  image: string;
}

const RecommendPage: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const userId = "user123"; // you can make this dynamic later

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/recommend/${userId}`);
        if (!response.ok) throw new Error("Failed to fetch recommendations");
        const data = await response.json();
        setRecommendations(data.recommendations || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-screen text-lg">Loading recommendations...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 mt-8">⚠️ {error}</div>;
  }

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">✨ Recommended for You</h1>
        <Link
          to="/"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-md transition"
        >
          ← Back to Products
        </Link>
      </div>

      {recommendations.length === 0 ? (
        <div className="text-center text-gray-600 mt-10">
          <p>No personalized recommendations yet 😢</p>
          <p className="text-sm mt-2">Try liking a few products first!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {recommendations.map((product) => (
            <div
              key={product._id}
              className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-transform hover:-translate-y-1 p-4"
            >
              <div className="h-48 flex justify-center items-center overflow-hidden mb-4">
                <img
                  src={product.image}
                  alt={product.title}
                  className="h-full object-contain rounded-lg"
                />
              </div>
              <h2 className="text-lg font-semibold text-gray-800 line-clamp-2 mb-1">
                {product.title}
              </h2>
              <p className="text-sm text-gray-500 mb-2">{product.category}</p>
              <div className="flex justify-between items-center">
                <span className="text-blue-600 font-bold">${product.price.toFixed(2)}</span>
                <span className="text-yellow-500 text-sm">⭐ {product.rating}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecommendPage;
