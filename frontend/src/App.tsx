import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import ProductsPage from "./components/ProductPage";
import RecommendPage from "./components/RecommendPage";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="p-4 bg-gray-800 text-white flex gap-6">
        <Link to="/">Products</Link>
        <Link to="/recommend">Recommendations</Link>
      </nav>

      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/recommend" element={<RecommendPage />} />
      </Routes>
    </BrowserRouter>
  );
}