import React, { useState, useEffect } from "react";
import ProductCard from "./ProductCard";
import type { Product } from "../types/Product";

interface RecommendResponse {
  recommendation: string;
}

const Home: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [price, setPrice] = useState<string>("");
  const [recommendation, setRecommendation] = useState<string>("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ price: parseFloat(price) }),
    });

    const data: RecommendResponse = await res.json();
    setRecommendation(data.recommendation);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">🛒 AI Product Recommender</h1>

      <form onSubmit={handleSubmit} className="mb-6">
        <input
          type="number"
          placeholder="Enter price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          className="border p-2 rounded mr-2"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Recommend
        </button>
      </form>

      {recommendation && (
        <div className="mb-6">
          <h3 className="text-lg font-medium">
            Recommendation:{" "}
            <span className="text-green-600 font-semibold">
              {recommendation}
            </span>
          </h3>
        </div>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
};

export default Home;
