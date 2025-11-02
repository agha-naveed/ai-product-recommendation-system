import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProductsPage from "./pages/ProductPage";
import RecommendationsPage from "./pages/RecommendationPage";

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<ProductsPage />} />
      <Route path="/recommendations" element={<RecommendationsPage />} />
    </Routes>
  </BrowserRouter>
);

export default App;
