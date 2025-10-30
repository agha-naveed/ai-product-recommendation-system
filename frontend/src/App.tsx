import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { FaStar } from "react-icons/fa";

interface Product {
  _id: string;
  title: string;
  category: string;
  price: number;
  rating: number;
  image: string;
}

const API_BASE = "http://localhost:8000";

const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selected, setSelected] = useState<Product | null>(null);
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const userId = "user123"; // demo user

  // Fetch all products
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await axios.get<Product[]>(`${API_BASE}/products`);
        setProducts(res.data);
      } catch (err) {
        console.error("❌ Error fetching products:", err);
      }
    };
    fetchProducts();
  }, []);

  // Handle product view
  const handleView = async (product: Product) => {
    setSelected(product);
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/view`, {
        user_id: userId,
        product_id: product._id,
      });
      const res = await axios.get<{ recommendations: Product[] }>(
        `${API_BASE}/recommend/${userId}`
      );
      setRecommendations(res.data.recommendations);
    } catch (err) {
      console.error("❌ Error fetching recommendations:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-200 text-gray-800">
      {/* Header */}
      <header className="p-6 text-center bg-white shadow-md sticky top-0 z-10">
        <h1 className="text-3xl font-bold text-indigo-600">
          🛍 Personalized Product Recommender
        </h1>
        <p className="text-gray-500">Built with React + TypeScript + FastAPI</p>
      </header>

      {/* Product Grid */}
      <div className="max-w-7xl mx-auto p-6 grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((p) => (
          <motion.div
            key={p._id}
            onClick={() => handleView(p)}
            whileHover={{ scale: 1.05 }}
            className="cursor-pointer bg-white rounded-2xl shadow-md hover:shadow-xl p-4 border border-gray-100 transition-all"
          >
            <img
              src={p.image}
              alt={p.title}
              className="h-48 w-full object-contain mb-3 rounded-xl"
            />
            <h3 className="font-semibold text-lg truncate">{p.title}</h3>
            <p className="text-sm text-gray-500 mb-2">{p.category}</p>
            <div className="flex items-center justify-between">
              <p className="text-indigo-600 font-bold text-lg">${p.price}</p>
              <span className="flex items-center text-yellow-500">
                <FaStar className="mr-1" /> {p.rating.toFixed(1)}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Recommendation Section */}
      {selected && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.4 }}
          className="fixed bottom-0 left-0 w-full bg-white shadow-xl border-t p-6"
        >
          <h2 className="text-2xl font-bold mb-3 text-indigo-600">
            Because you viewed: {selected.title}
          </h2>

          {loading ? (
            <p className="text-gray-500">Fetching personalized recommendations...</p>
          ) : recommendations.length > 0 ? (
            <div className="flex overflow-x-auto gap-6 pb-3">
              {recommendations.map((r) => (
                <motion.div
                  key={r._id}
                  whileHover={{ scale: 1.05 }}
                  className="min-w-[200px] bg-gray-50 p-3 rounded-2xl border shadow-sm hover:shadow-md"
                >
                  <img
                    src={r.image}
                    alt={r.title}
                    className="h-32 w-full object-contain mb-2 rounded-xl"
                  />
                  <h3 className="font-semibold truncate">{r.title}</h3>
                  <p className="text-sm text-gray-500">{r.category}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className="font-bold text-indigo-600">${r.price}</p>
                    <span className="flex items-center text-yellow-500 text-sm">
                      <FaStar className="mr-1" /> {r.rating.toFixed(1)}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No recommendations yet.</p>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default App;