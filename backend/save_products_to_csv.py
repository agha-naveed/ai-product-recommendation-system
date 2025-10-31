import requests
import pandas as pd

def fetch_data():
    urls = [
        "https://fakestoreapi.com/products",
        "https://dummyjson.com/products",
        "https://api.escuelajs.co/api/v1/products",
    ]
    
    all_data = []

    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()

            # Normalize API structure
            if "products" in data:  # dummyjson
                data = data["products"]

            for item in data:
                all_data.append({
                    "id": item.get("id"),
                    "title": item.get("title") or item.get("name"),
                    "price": item.get("price", 0),
                    "category": (
                        item.get("category").get("name")
                        if isinstance(item.get("category"), dict)
                        else item.get("category")
                    ),
                    "rating": (
                        item.get("rating", {}).get("rate")
                        if isinstance(item.get("rating"), dict)
                        else item.get("rating", 3)
                    ),
                    "image": (
                        item.get("image")
                        or (item.get("images")[0] if isinstance(item.get("images"), list) else "")
                    )
                })
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    print(f"Fetched {len(df)} total products.")
    df.to_csv("products.csv", index=False)
    print("Saved as products.csv ✅")

if __name__ == "__main__":
    fetch_data()
