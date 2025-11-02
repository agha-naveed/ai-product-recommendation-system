import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

interface Product {
  title?: string;
  name?: string;
  price: number;
  category?: string | { name: string };
  rating?: number | { rate: number };
  image?: string;
  images?: string[];
}

export default function ProductCard({ product }: { product: Product }) {
  const navigate = useNavigate();

  const handleRecommend = async () => {
    try {
      const response = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: product.title || product.name,
          price: product.price,
          category:
            typeof product.category === "object"
              ? product.category.name
              : product.category,
          rating:
            typeof product.rating === "object"
              ? product.rating.rate
              : product.rating,
        }),
      });

      const recs = await response.json();
      localStorage.setItem("recommendations", JSON.stringify(recs));
      localStorage.setItem("selectedProduct", JSON.stringify(product));
      navigate("/recommendations");
    } catch (error) {
      console.error("Recommendation fetch failed:", error);
    }
  };

  return (
    <motion.div
      className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-4 hover:shadow-cyan-500/20 transition-all cursor-pointer"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="flex flex-col items-center">
        <img
          src={product.image || product.images?.[0]}
          alt={product.title || product.name}
          className="w-full h-48 object-contain rounded-lg mb-4 bg-gray-900"
        />
        <h2 className="text-lg font-semibold text-gray-100 text-center line-clamp-2">
          {product.title || product.name}
        </h2>
        <p className="text-cyan-400 font-medium mt-1">${product.price}</p>
        <p className="text-gray-400 text-sm mt-1">
          ⭐ {typeof product.rating === "object" ? product.rating.rate : product.rating}
        </p>
        <p className="text-xs text-gray-500 mt-1 italic">
          {typeof product.category === "object"
            ? product.category.name
            : product.category}
        </p>
        <motion.button
          onClick={handleRecommend}
          className="mt-3 px-5 py-2 rounded-lg bg-cyan-500 text-white hover:bg-cyan-600 transition"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Get Recommendations
        </motion.button>
      </div>
    </motion.div>
  );
}
