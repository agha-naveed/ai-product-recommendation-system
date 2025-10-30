from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Database ==========
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
products_col = db["products"]
users_col = db["users"]

# ========== Helper Functions ==========
def build_feature_matrix():
    products = list(products_col.find({}, {"_id": 1, "category": 1, "price": 1, "rating": 1}))
    df = pd.DataFrame(products)

    # Handle empty database case
    if df.empty:
        return pd.DataFrame(), np.array([]), None, None

    le = LabelEncoder()
    df["category_encoded"] = le.fit_transform(df["category"].astype(str))

    X = df[["price", "rating", "category_encoded"]].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return df, X_scaled, scaler, le

# ========== Routes ==========
@app.get("/products")
def get_products():
    products = list(products_col.find({}, {"_id": 1, "title": 1, "category": 1, "price": 1, "rating": 1, "image": 1}))
    for p in products:
        p["_id"] = str(p["_id"])
    return products


@app.post("/like")
def like_product(data: dict):
    user_id = data["user_id"]
    product_id = data["product_id"]
    users_col.update_one(
        {"user_id": user_id},
        {"$addToSet": {"liked_products": str(product_id)}},
        upsert=True
    )
    return {"message": "Product liked successfully!"}


@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    user = users_col.find_one({"user_id": user_id})
    if not user or "liked_products" not in user or len(user["liked_products"]) == 0:
        return {"message": "No likes yet", "recommendations": []}

    liked_ids = [ObjectId(pid) for pid in user["liked_products"] if ObjectId.is_valid(pid)]

    # Build feature matrix from database
    df, X, scaler, le = build_feature_matrix()
    if X is None or df.empty:
        return {"message": "No products available", "recommendations": []}

    # Get liked products
    liked_df = df[df["_id"].isin(liked_ids)]
    if liked_df.empty:
        return {"message": "Liked products not found", "recommendations": []}

    # ✅ Step 1: Find dominant category among liked items
    top_category = liked_df["category"].value_counts().idxmax()

    # ✅ Step 2: Focus only on products from that category
    liked_df = liked_df[liked_df["category"] == top_category]

    # ✅ Step 3: Average vector for that category
    liked_vectors = X[liked_df.index]
    user_vector = np.mean(liked_vectors, axis=0).reshape(1, -1)

    # ✅ Step 4: Fit KNN (cosine distance)
    knn = NearestNeighbors(metric="cosine", n_neighbors=min(10, len(df)))
    knn.fit(X)

    # ✅ Step 5: Find nearest neighbors
    distances, indices = knn.kneighbors(user_vector)
    recs = df.iloc[indices[0]]

    # ✅ Step 6: Remove already liked items
    recs = recs[~recs["_id"].isin(liked_ids)]

    # ✅ Step 7: Convert results for frontend
    recs = recs.to_dict(orient="records")
    for r in recs:
        r["_id"] = str(r["_id"])

    return {
        "message": f"Recommended from your favorite category: {top_category}",
        "recommendations": recs
    }

