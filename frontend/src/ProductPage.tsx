import React, { useEffect, useState } from "react";
import axios from "axios";

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

  useEffect(() => {
    const fetchProducts = async () => {
      const res = await axios.get("http://localhost:5000/products");
      setProducts(res.data);
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
    const res = await axios.post("http://localhost:5000/recommend", payload);
    localStorage.setItem("recommendations", JSON.stringify(res.data));
    window.location.href = "/recommendations";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 p-6">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center tracking-tight">
        🛍️ AI Product Explorer
      </h1>

      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {products.map((p, i) => (
          <div
            key={"products-"+i}
            className="group bg-white rounded-2xl shadow hover:shadow-2xl transition transform hover:-translate-y-1 overflow-hidden cursor-pointer"
            onClick={() => handleRecommend(p)}
          >
            <img
              src={p.image || p.images?.[0]}
              alt={p.title || p.name || "Product"}
              className="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div className="p-4">
              <h2 className="text-lg font-semibold truncate text-gray-900">
                {p.title || p.name}
              </h2>
              <p className="text-gray-500 mb-1">
                {typeof p.category === "object"
                  ? p.category.name
                  : p.category || "Unknown"}
              </p>
              <p className="text-indigo-600 font-bold text-lg">
                ${p.price?.toFixed(2) ?? "N/A"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductsPage;
