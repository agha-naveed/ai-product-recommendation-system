from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

app = FastAPI()

# ====== CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== MongoDB ======
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
products_col = db["products"]
users_col = db["users"]


# ====== Helper: Build Product Feature Matrix ======
def build_feature_matrix():
    products = list(products_col.find({}, {"_id": 1, "title": 1, "category": 1, "price": 1, "rating": 1}))
    df = pd.DataFrame(products)
    if df.empty:
        return df, None, None

    # Fill missing values
    df["title"] = df["title"].fillna("")
    df["category"] = df["category"].fillna("other")
    df["price"] = df["price"].fillna(df["price"].mean())
    df["rating"] = df["rating"].fillna(0)

    # ----- 1️⃣ One-hot encode categories -----
    encoder = OneHotEncoder()
    category_encoded = encoder.fit_transform(df[["category"]]).toarray()

    # ----- 2️⃣ TF-IDF for titles -----
    tfidf = TfidfVectorizer(max_features=50, stop_words="english")
    title_tfidf = tfidf.fit_transform(df["title"])

    # ----- 3️⃣ Combine all features -----
    numeric_features = df[["price", "rating"]].values
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(numeric_features)

    # Combine all into one large matrix
    X = np.hstack([numeric_scaled, category_encoded, title_tfidf.toarray()])

    return df, X, scaler


@app.get("/products")
def get_products():
    products = list(products_col.find({}, {"_id": 1, "title": 1, "price": 1, "rating": 1, "category": 1, "image": 1}))
    for p in products:
        p["_id"] = str(p["_id"])
    return products


@app.post("/view")
def add_view(data: dict):
    user_id = data["user_id"]
    product_id = data["product_id"]

    try:
        product = products_col.find_one({"_id": ObjectId(product_id)})
    except:
        return {"error": "Invalid product ID"}

    if not product:
        return {"error": "Product not found"}

    users_col.update_one(
        {"user_id": user_id},
        {"$addToSet": {"viewed_products": str(product["_id"])}},
        upsert=True
    )

    return {"message": "View saved", "product": product["title"]}


@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    user = users_col.find_one({"user_id": user_id})
    if not user or "viewed_products" not in user or not user["viewed_products"]:
        return {"recommendations": []}

    last_viewed_id = user["viewed_products"][-1]

    # Rebuild matrix
    df, X, scaler = build_feature_matrix()
    if df.empty:
        return {"recommendations": []}

    # Fit KNN
    knn = NearestNeighbors(n_neighbors=8, metric="cosine")
    knn.fit(X)

    # Find last viewed product
    try:
        target = df[df["_id"] == ObjectId(last_viewed_id)]
    except:
        return {"recommendations": []}

    if target.empty:
        return {"recommendations": []}

    target_index = target.index[0]
    distances, indices = knn.kneighbors([X[target_index]])

    # Collect recommended products
    recs = df.iloc[indices[0][1:6]]  # skip the first one (same product)

    # Filter out already viewed
    viewed_ids = [ObjectId(pid) for pid in user["viewed_products"] if ObjectId.is_valid(pid)]
    recs = recs[~recs["_id"].isin(viewed_ids)]

    # Get full details
    recs = list(products_col.find({"_id": {"$in": recs["_id"].tolist()}}))
    for r in recs:
        r["_id"] = str(r["_id"])

    return {"recommendations": recs}
