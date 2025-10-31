// frontend/src/pages/ProductsPage.jsx
import { useEffect, useState } from 'react';
import ProductCard from './ProductCard';

export default function ProductsPage() {
  const [products, setProducts] = useState<any>([]);

  useEffect(() => {
    async function fetchProducts() {
      const res1 = await fetch('https://fakestoreapi.com/products');
      const res2 = await fetch('https://dummyjson.com/products?limit=100');
      const res3 = await fetch('https://api.escuelajs.co/api/v1/products');

      const data1 = await res1.json();
      const data2 = await res2.json();
      const data3 = await res3.json();

      const allProducts = [
        ...data1,
        ...data2.products,
        ...data3.slice(0, 80)
      ];

      setProducts(allProducts.slice(0, 200)); // limit to 200
    }

    fetchProducts();
  }, []);

  return (
    <div className="grid grid-cols-4 gap-4 p-4">
      {products.map((p:any, idx:number) => (
        <ProductCard key={idx} product={p} />
      ))}
    </div>
  );
}
