import React from "react";
import type { Product } from "../types/Product";

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <div className="border p-4 rounded-xl shadow-sm hover:shadow-lg transition">
      <img
        src={product.image || product.thumbnail}
        alt={product.title}
        className="h-32 w-full object-contain mb-3"
      />
      <h3 className="font-semibold">{product.title}</h3>
      <p className="text-gray-600">${product.price}</p>
      {product.rating && (
        <p className="text-yellow-500 text-sm">⭐ {product.rating}</p>
      )}
    </div>
  );
};

export default ProductCard;
