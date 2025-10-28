import axios from 'axios';
const BASE_URL = 'http://127.0.0.1:8000';

export const getProducts = async () => {
  const res = await axios.get(`${BASE_URL}/products`);
  return res.data.products;
};

export const getRecommendations = async (productId) => {
  const res = await axios.get(`${BASE_URL}/recommend/${productId}`);
  return res.data.recommendations;
};
