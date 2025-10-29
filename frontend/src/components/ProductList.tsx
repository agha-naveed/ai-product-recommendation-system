export default function ProductList({ product, onRecommend }:any) {
  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden p-3 hover:shadow-xl transition">
      <img
        src={product.image}
        alt={product.title}
        className="w-full h-40 object-contain mb-2"
      />
      <h3 className="text-sm font-semibold">{product.title}</h3>
      <p className="text-gray-600 text-sm">${product.price}</p>
      <p className="text-yellow-600 text-xs">⭐ {product.rating}</p>
      <button
        onClick={onRecommend}
        className="bg-blue-500 text-white text-sm mt-2 px-3 py-1 rounded hover:bg-blue-600"
      >
        Recommend
      </button>
    </div>
  );
}
