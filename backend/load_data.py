import requests
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["productDB"]
collection = db["products"]

# Fetch data from FakeStoreAPI
url = "https://fakestoreapi.com/products"
response = requests.get(url)
data = response.json()

# Insert into MongoDB
for item in data:
    doc = {
        "name": item["title"],
        "price": item["price"],
        "rating": item.get("rating", {}).get("rate", 0),
        "category": item["category"],
        "image": item["image"],  # 🖼️ image URL
        "description": item["description"]
    }
    collection.insert_one(doc)

print("✅ Products added to MongoDB:", collection.count_documents({}))
