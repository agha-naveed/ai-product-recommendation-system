import React, { useEffect, useState } from 'react';
import { getProducts, getRecommendations } from '../api';

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    getProducts().then(setProducts);
  }, []);

  const handleClick = (id) => {
    getRecommendations(id).then(setRecs);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Products</h2>
      <div className="grid grid-cols-3 gap-4">
        {products.map(p => (
          <div key={p._id} className="p-3 border rounded" onClick={() => handleClick(p._id)}>
            <h3>{p.name}</h3>
            <p>Price: ${p.price}</p>
            <p>Rating: {p.rating}</p>
          </div>
        ))}
      </div>

      {recs.length > 0 && (
        <>
          <h2 className="text-xl font-bold mt-8 mb-4">Recommended Products</h2>
          <div className="grid grid-cols-3 gap-4">
            {recs.map(r => (
              <div key={r._id} className="p-3 border rounded bg-gray-100">
                <h3>{r.name}</h3>
                <p>Price: ${r.price}</p>
                <p>Rating: {r.rating}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
