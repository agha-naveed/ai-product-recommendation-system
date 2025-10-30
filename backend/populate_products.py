import requests
from pymongo import MongoClient

# ========== MongoDB Setup ==========
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
collection = db["products"]

# Clear existing data
collection.delete_many({})
print("🧹 Old product data cleared!")

# ========== Helper Function ==========
def fetch_api(url, mapper):
    """Fetch data and map to our schema."""
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return [mapper(item) for item in data if item]
    except Exception as e:
        print(f"⚠️ Error fetching from {url}: {e}")
        return []

# ========== API Mappers ==========

def map_fakestore(item):
    return {
        "title": item["title"],
        "category": item["category"],
        "price": float(item["price"]),
        "rating": float(item.get("rating", {}).get("rate", 4.0)),
        "image": item["image"],
    }

def map_dummyjson(item):
    return {
        "title": item["title"],
        "category": item["category"],
        "price": float(item["price"]),
        "rating": float(item.get("rating", 4.0)),
        "image": item["thumbnail"],
    }

def map_escuelajs(item):
    price = float(item.get("price", 0))
    category = item.get("category", {}).get("name", "Unknown")
    image = item.get("images", [""])[0] if item.get("images") else ""
    return {
        "title": item["title"],
        "category": category,
        "price": price,
        "rating": 4.0,
        "image": image,
    }

# ========== Fetch From APIs ==========
products = []

print("📦 Fetching from FakeStoreAPI...")
products += fetch_api("https://fakestoreapi.com/products", map_fakestore)

print("🧥 Fetching from DummyJSON...")
dummy_data = requests.get("https://dummyjson.com/products?limit=100").json()["products"]
products += [map_dummyjson(p) for p in dummy_data]

print("💍 Fetching from Escuelajs...")
products += fetch_api("https://api.escuelajs.co/api/v1/products", map_escuelajs)

# ========== Save to MongoDB ==========
# Remove duplicates by title
unique_titles = set()
unique_products = []
for p in products:
    if p["title"] not in unique_titles and p["image"]:
        unique_titles.add(p["title"])
        unique_products.append(p)

collection.insert_many(unique_products)
print(f"✅ Inserted {len(unique_products)} unique products into MongoDB!")
