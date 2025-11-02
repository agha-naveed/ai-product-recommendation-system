import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

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

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await axios.get("http://localhost:8000/products");
        setProducts(res.data);
      } catch (err) {
        console.error("Error fetching products:", err);
      }
    };
    fetchProducts();
  }, []);

  const handleRecommend = async (p: Product) => {
    const payload = {
      price: p.price ?? 500,
      rating: typeof p.rating === "object" ? p.rating.rate : p.rating ?? 3,
      category:
        typeof p.category === "object"
          ? p.category.name
          : p.category ?? "Electronics",
    };

    const res = await axios.post("http://localhost:8000/recommend", payload);
    localStorage.setItem("recommendations", JSON.stringify(res.data));
    localStorage.setItem("selectedProduct", JSON.stringify(p)); // store selected product
    navigate("/recommendations");
  };

  return (
    <motion.div
      className="min-h-screen bg-slate-800 text-gray-100 p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-4xl md:text-5xl font-extrabold text-center mb-10 text-cyan-400 tracking-tight">
        🛍️ AI Product Explorer
      </h1>

      {products.length === 0 ? (
        <div className="flex justify-center items-center h-64 text-gray-400 text-lg">
          Loading products...
        </div>
      ) : (
        <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map((p, i) => (
            <motion.div
              key={"product-" + i}
              className="bg-gray-700 rounded-2xl shadow-md hover:shadow-white/10 overflow-hidden transition transform hover:-translate-y-2 cursor-pointer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              transition={{ type: "spring", stiffness: 200, damping: 10 }}
              onClick={() => handleRecommend(p)}
            >
              <div className="relative">
                <img
                  src={p.image || p.images?.[0]}
                  alt={p.title || p.name || "Product"}
                  className="w-full h-56 object-contain bg-gray-900 p-4"
                />
                <motion.div
                  className="absolute inset-0 bg-cyan-500/0 group-hover:bg-cyan-500/5 transition-all"
                  initial={{ opacity: 0 }}
                  whileHover={{ opacity: 1 }}
                />
              </div>

              <div className="p-4 text-center">
                <h2 className="text-lg font-semibold truncate">
                  {p.title || p.name}
                </h2>
                <p className="text-gray-400 text-sm mt-1">
                  {typeof p.category === "object"
                    ? p.category.name
                    : p.category || "Unknown"}
                </p>
                <p className="text-cyan-400 text-xl font-bold mt-1">
                  ${p.price?.toFixed(2) ?? "N/A"}
                </p>
                <p className="text-gray-500 text-sm mt-1">
                  ⭐{" "}
                  {typeof p.rating === "object"
                    ? p.rating.rate
                    : p.rating ?? "3.0"}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default ProductsPage;
