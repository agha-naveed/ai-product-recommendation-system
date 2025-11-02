import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

interface Product {
  id?: number;
  title?: string;
  name?: string;
  price?: number;
  image?: string;
  rating?: number | { rate: number };
  images?: string[];
  category?: string | { name: string };
}

const RecommendationsPage: React.FC = () => {
  const [recs, setRecs] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  useEffect(() => {
    const data = localStorage.getItem("recommendations");
    const selected = localStorage.getItem("selectedProduct");
    if (data) setRecs(JSON.parse(data));
    if (selected) setSelectedProduct(JSON.parse(selected));
  }, []);

  return (
    <motion.div
      className="min-h-screen bg-gray-900 text-gray-100 p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-3xl md:text-4xl font-bold text-center mb-10 text-cyan-400">
        🌟 Your AI-Powered Recommendations
      </h1>

      {/* Selected Product Preview */}
      {selectedProduct && (
        <motion.div
          className="max-w-3xl mx-auto mb-10 bg-gray-800 p-6 rounded-2xl shadow-lg flex flex-col md:flex-row items-center gap-6"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <img
            src={selectedProduct.image || selectedProduct.images?.[0]}
            alt={selectedProduct.title || selectedProduct.name}
            className="w-40 h-40 object-contain rounded-xl bg-gray-900"
          />
          <div className="text-center md:text-left">
            <h2 className="text-2xl font-semibold">
              {selectedProduct.title || selectedProduct.name}
            </h2>
            <p className="text-cyan-400 text-lg font-medium mt-1">
              ${selectedProduct.price?.toFixed(2)}
            </p>
            <p className="text-gray-400 mt-1">
              ⭐{" "}
              {typeof selectedProduct.rating === "object"
                ? selectedProduct.rating.rate
                : selectedProduct.rating}
            </p>
            <p className="text-xs text-gray-500 mt-1 italic">
              {typeof selectedProduct.category === "object"
                ? selectedProduct.category.name
                : selectedProduct.category}
            </p>
          </div>
        </motion.div>
      )}

      {/* Recommendation Grid */}
      <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {recs.map((p, i) => (
          <motion.div
            key={"rec-" + i}
            className="bg-gray-800 rounded-2xl shadow-md hover:shadow-cyan-500/20 overflow-hidden transition transform hover:-translate-y-2 cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
            transition={{ type: "spring", stiffness: 200, damping: 10 }}
          >
            <img
              src={p.image || p.images?.[0]}
              alt={p.title || p.name}
              className="w-full h-48 object-contain bg-gray-900 p-4"
            />
            <div className="p-4 text-center">
              <h2 className="text-lg font-semibold truncate">
                {p.title || p.name}
              </h2>
              <p className="text-gray-400 text-sm mt-1">
                ⭐{" "}
                {typeof p.rating === "object"
                  ? p.rating.rate
                  : p.rating}
              </p>
              <p className="text-cyan-400 text-xl font-bold mt-1">
                ${p.price?.toFixed(2)}
              </p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Back Button */}
      <div className="text-center mt-12">
        <Link
          to="/"
          className="inline-block bg-cyan-500 hover:bg-cyan-600 text-white px-6 py-2 rounded-xl transition transform hover:scale-105 shadow-lg"
        >
          ← Back to Products
        </Link>
      </div>
    </motion.div>
  );
};

export default RecommendationsPage;