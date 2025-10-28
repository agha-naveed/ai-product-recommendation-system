import axios from "axios";
const BASE_URL = "http://127.0.0.1:8000";

export async function getProducts() {
  const res = await axios.get(`${BASE_URL}/products`);
  return res.data.products;
}

export async function getRecommendations(id:number) {
  const res = await axios.get(`${BASE_URL}/recommend/${id}`);
  return res.data.recommendations;
}