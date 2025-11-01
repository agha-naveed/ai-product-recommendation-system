// frontend/src/components/ProductCard.jsx
export default function ProductCard({ product }:any) {
  const handleRecommend = async () => {
    const response = await fetch('http://localhost:8000/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: product.title || product.name,
        price: product.price,
        category: product.category?.name || product.category,
        rating: product.rating?.rate || product.rating
      })
    });
    const recs = await response.json();
    localStorage.setItem('recommendations', JSON.stringify(recs));
    window.location.href = '/recommendations';
  };

  return (
    <div className="border p-2 shadow-md rounded">
      <img src={product.image || product.images?.[0]} alt={product.title} className="w-full h-40 object-cover" />
      <h2 className="text-lg font-bold mt-2">{product.title || product.name}</h2>
      <p>${product.price}</p>
      <button
        onClick={handleRecommend}
        className="mt-2 bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
      >
        Get Recommendations
      </button>
    </div>
  );
}
