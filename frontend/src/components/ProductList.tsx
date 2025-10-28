import { useEffect, useState } from "react";
import { getProducts, getRecommendations } from "../api";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    getProducts().then(setProducts);
  }, []);

  const handleClick = (id:number) => {
    getRecommendations(id).then(setRecs);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">🛒 Products</h1>
      <div className="grid grid-cols-4 gap-4">
        {products.map((p:any) => (
          <div
            key={p._id}
            onClick={() => handleClick(p._id)}
            className="border rounded-lg p-2 hover:shadow-lg cursor-pointer"
          >
            <img src={p.image} alt={p.name} className="h-40 w-full object-contain mb-2" />
            <h2 className="text-sm font-semibold">{p.name}</h2>
            <p>${p.price}</p>
            <p>⭐ {p.rating}</p>
          </div>
        ))}
      </div>

      {recs.length > 0 && (
        <>
          <h2 className="text-xl font-bold mt-6 mb-4">Recommended Products</h2>
          <div className="grid grid-cols-4 gap-4">
            {recs.map((r:any) => (
              <div key={r._id} className="border rounded-lg p-2 bg-gray-100">
                <img src={r.image} alt={r.name} className="h-40 w-full object-contain mb-2" />
                <h2 className="text-sm font-semibold">{r.name}</h2>
                <p>${r.price}</p>
                <p>⭐ {r.rating}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
