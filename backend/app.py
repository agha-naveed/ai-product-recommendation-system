from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

# CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
collection = db["products"]

# ========== Utility ==========
def get_dataframe():
    products = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(products)
    return df

# ========== Routes ==========

@app.get("/")
def home():
    return {"message": "🧠 Product Recommender API Running!"}

@app.get("/products")
def get_products():
    products = list(collection.find({}, {"_id": 0}))
    return {"count": len(products), "data": products}

@app.get("/recommend")
def recommend_product(title: str, k: int = 6):
    df = get_dataframe()
    if title not in df["title"].values:
        return {"error": "Product not found"}

    # Encode categories
    encoder = OneHotEncoder(sparse_output=False)
    cat_encoded = encoder.fit_transform(df[["category"]])
    cat_df = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(["category"]))
    df = pd.concat([df, cat_df], axis=1)

    features = ["price", "rating"] + list(cat_df.columns)
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit KNN
    model = NearestNeighbors(n_neighbors=min(k, len(df)), metric="cosine")
    model.fit(X_scaled)

    # Find target index
    idx = df[df["title"] == title].index[0]
    distances, indices = model.kneighbors([X_scaled[idx]])

    # Prepare response
    results = []
    for i in indices[0][1:]:
        results.append({
            "title": df.iloc[i]["title"],
            "category": df.iloc[i]["category"],
            "price": df.iloc[i]["price"],
            "rating": df.iloc[i]["rating"],
            "image": df.iloc[i]["image"]
        })

    return {"target": title, "recommended": results}