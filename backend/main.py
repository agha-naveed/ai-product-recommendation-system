# backend/main.py
from fastapi import FastAPI
from app.services.fetch_data import fetch_and_store_products
from app.models.train_model import train_model
from app.models.recommend import recommend_product
from app.db import products_collection
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Fetch products if MongoDB is empty
    if await products_collection.count_documents({}) == 0:
        print("📦 Fetching products...")
        await fetch_and_store_products()
    
    # Train model if not found
    if not os.path.exists("app/models/model.pkl"):
        print("🧠 Training model...")
        await train_model()

@app.get("/products")
async def get_products():
    return await products_collection.find().to_list(length=20)

@app.get("/recommend")
async def recommend(price: float):
    result = recommend_product(price)
    return {"recommendation": result}
