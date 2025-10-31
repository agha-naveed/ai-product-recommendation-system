# backend/app/services/fetch_data.py
import requests
from app.db import products_collection
import asyncio

async def fetch_and_store_products():
    urls = [
        "https://fakestoreapi.com/products",
        "https://dummyjson.com/products?limit=100",
        "https://api.escuelajs.co/api/v1/products"
    ]

    all_products = []

    for url in urls:
        try:
            print(f"📡 Fetching from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Handle each API structure
            if isinstance(data, dict) and "products" in data:
                all_products.extend(data["products"])
            elif isinstance(data, list):
                all_products.extend(data)
        except Exception as e:
            print(f"❌ Error fetching from {url}: {e}")

    print(f"✅ Total products fetched: {len(all_products)}")

    if all_products:
        await products_collection.delete_many({})
        await products_collection.insert_many(all_products)
        print("✅ Products inserted into MongoDB successfully!")
    else:
        print("⚠️ No data to insert into MongoDB!")

asyncio.run(fetch_and_store_products())