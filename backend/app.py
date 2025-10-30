from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
    df, X = build_feature_matrix()
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



@app.get("/recommend/graph/{user_id}")
def recommend_graph(user_id: str):
    user = users_col.find_one({"user_id": user_id})
    if not user or "liked_products" not in user or len(user["liked_products"]) == 0:
        raise HTTPException(status_code=404, detail="No liked products yet")

    liked_ids = [ObjectId(pid) for pid in user["liked_products"] if ObjectId.is_valid(pid)]

    df, X_scaled, scaler, le = build_feature_matrix()
    if df.empty:
        raise HTTPException(status_code=404, detail="No products in DB")

    # Prepare feature space (price vs rating)
    liked_df = df[df["_id"].isin(liked_ids)]

    # Get recommendations using your improved logic
    top_category = liked_df["category"].value_counts().idxmax()
    liked_df = liked_df[liked_df["category"] == top_category]
    liked_vectors = X_scaled[liked_df.index]
    user_vector = np.mean(liked_vectors, axis=0).reshape(1, -1)

    knn = NearestNeighbors(metric="cosine", n_neighbors=min(10, len(df)))
    knn.fit(X_scaled)
    distances, indices = knn.kneighbors(user_vector)
    recs = df.iloc[indices[0]]
    recs = recs[~recs["_id"].isin(liked_ids)]

    # --- Plot the graph ---
    plt.figure(figsize=(8, 6))

    # Plot all points
    plt.scatter(df["price"], df["rating"], color="gray", alpha=0.4, label="All Products")

    # Plot liked items
    plt.scatter(liked_df["price"], liked_df["rating"], color="green", s=80, label="Liked Products")

    # Plot recommended items
    plt.scatter(recs["price"], recs["rating"], color="red", s=80, label="Recommended")

    plt.xlabel("Price")
    plt.ylabel("Rating")
    plt.title(f"Recommendation Map for {user_id}")
    plt.legend()

    # Convert plot to base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return {"graph": f"data:image/png;base64,{image_base64}"}