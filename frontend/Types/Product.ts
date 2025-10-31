export interface Product {
  id: number | string;
  title: string;
  price: number;
  description?: string;
  category?: string;
  image?: string;
  thumbnail?: string;
  rating?: number;
}
