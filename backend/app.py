from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
import pandas as pd

app = FastAPI()

# ========== Database ==========
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
products_col = db["products"]
users_col = db["users"]

# ========== Data Model ==========
class UserAction(BaseModel):
    user_id: str
    product_id: str

# ========== Helper: Build Product Features ==========
def build_feature_matrix():
    products = list(products_col.find({}, {"_id": 1, "category": 1, "price": 1, "rating": 1}))
    df = pd.DataFrame(products)

    le = LabelEncoder()
    df["category_encoded"] = le.fit_transform(df["category"])

    X = df[["price", "rating", "category_encoded"]].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return df, X_scaled, scaler, le

# ========== KNN Model ==========
df, X_scaled, scaler, le = build_feature_matrix()
knn = NearestNeighbors(metric="euclidean")
knn.fit(X_scaled)

# ========== Record User Actions ==========
@app.post("/view")
def record_view(data: UserAction):
    user = users_col.find_one({"_id": data.user_id})
    if not user:
        users_col.insert_one({"_id": data.user_id, "viewed_products": [data.product_id]})
    else:
        users_col.update_one({"_id": data.user_id}, {"$addToSet": {"viewed_products": data.product_id}})
    return {"msg": "View recorded"}

# ========== Get Personalized Recommendations ==========
@app.get("/recommend/{user_id}")
def personalized_recommendations(user_id: str, k: int = 5):
    user = users_col.find_one({"_id": user_id})
    if not user or not user.get("viewed_products"):
        raise HTTPException(404, "No user activity found")

    viewed_ids = user["viewed_products"]
    viewed_products = list(products_col.find({"_id": {"$in": [ObjectId(pid) for pid in viewed_ids]}}))

    if not viewed_products:
        raise HTTPException(404, "No viewed products found")

    # Build user profile (average of viewed features)
    user_df = pd.DataFrame(viewed_products)
    user_df["category_encoded"] = le.transform(user_df["category"])
    user_features = user_df[["price", "rating", "category_encoded"]].mean(axis=0).values
    user_features_scaled = scaler.transform([user_features])

    # Find K nearest products
    distances, indices = knn.kneighbors(user_features_scaled, n_neighbors=k+len(viewed_ids))
    recs = df.iloc[indices[0]]
    recs = recs[~df["_id"].isin([ObjectId(pid) for pid in viewed_ids])]  # remove already-viewed
    rec_products = list(products_col.find({"_id": {"$in": recs["_id"].tolist()}}))

    return {"user_id": user_id, "recommendations": rec_products}
