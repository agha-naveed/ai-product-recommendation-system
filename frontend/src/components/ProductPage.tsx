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

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/products").then(res => setProducts(res.data));
  }, []);

  const handleAction = async (id: string, action: string) => {
    await axios.post("http://localhost:8000/like", {
      user_id: "user123",
      product_id: id,
      action,
    });
  };

  return (
    <div className="grid grid-cols-4 gap-6 p-6">
      {products.map(p => (
        <div key={p._id} className="border rounded-xl shadow-md p-3 hover:shadow-lg transition">
          <img src={p.image} alt={p.title} className="h-48 w-full object-cover rounded-lg" />
          <h3 className="text-lg font-semibold mt-2">{p.title}</h3>
          <p className="text-sm text-gray-500">{p.category}</p>
          <p className="font-bold">${p.price}</p>
          <div className="flex gap-2 mt-2">
            <button onClick={() => handleAction(p._id, "like")} className="px-3 py-1 bg-green-500 text-white rounded-lg">👍 Like</button>
            <button onClick={() => handleAction(p._id, "dislike")} className="px-3 py-1 bg-red-500 text-white rounded-lg">👎 Dislike</button>
            <button onClick={() => handleAction(p._id, "view")} className="px-3 py-1 bg-blue-500 text-white rounded-lg">👀 View</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductsPage;