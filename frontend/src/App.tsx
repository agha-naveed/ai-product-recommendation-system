import { useEffect, useState } from "react";
import axios from "axios";
import ProductCard from "./components/ProductList";
import RecommendationList from "./components/RecommendationList";

const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend

function App() {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  // Load products
  useEffect(() => {
    axios.get(`${API_BASE}/products`).then((res) => {
      setProducts(res.data.data);
    });
  }, []);

  // Fetch recommendations
  const getRecommendations = async (title:any) => {
    setSelectedProduct(title);
    const res = await axios.get(`${API_BASE}/recommend`, { params: { title } });
    setRecommendations(res.data.recommended || []);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-8">🧠 Product Recommendation System</h1>

      {/* Product Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {products.map((p:any, i:number) => (
          <ProductCard
            key={i}
            product={p}
            onRecommend={() => getRecommendations(p.title)}
          />
        ))}
      </div>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <RecommendationList
          target={selectedProduct}
          recommendations={recommendations}
        />
      )}
    </div>
  );
}

export default App;