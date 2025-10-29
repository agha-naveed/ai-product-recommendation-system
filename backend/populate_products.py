import requests
import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
collection = db["products"]

# Clear old data (optional)
collection.delete_many({})
print("🧹 Cleared old products")

# Fetch data from FakeStoreAPI
response = requests.get("https://fakestoreapi.com/products")
if response.status_code != 200:
    raise Exception("❌ Failed to fetch from FakeStoreAPI")

base_products = response.json()
extra_products = []

# Generate extra variations
for p in base_products:
    for _ in range(10):  # 10 variations per product
        price = round(p["price"] * random.uniform(0.8, 1.2), 2)
        rating = round(random.uniform(2.5, 5.0), 1)
        color = random.choice(["Red", "Blue", "Green", "Black", "White"])
        size = random.choice(["S", "M", "L", "XL"])

        new_product = {
            "title": f"{p['title']} ({color}, {size})",
            "category": p["category"],
            "price": price,
            "rating": rating,
            "image": p["image"],
        }
        extra_products.append(new_product)

collection.insert_many(extra_products)
print(f"✅ Inserted {len(extra_products)} products into MongoDB!")