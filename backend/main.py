from fastapi import FastAPI
from pymongo import MongoClient
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["productDB"]
collection = db["products"]

# Load data
def load_data():
    data = list(collection.find())
    df = pd.DataFrame(data)
    df["_id"] = df["_id"].astype(str)
    return df

df = load_data()

# Encode category to numeric
df["category_code"] = df["category"].astype("category").cat.codes

# Build features (price, rating, category)
features = df[["price", "rating", "category_code"]]

model = NearestNeighbors(n_neighbors=6, metric="cosine")
model.fit(features)
joblib.dump(model, "knn_model.pkl")

@app.get("/products")
def get_products():
    items = list(collection.find({}, {"_id": 1, "name": 1, "price": 1, "image": 1, "rating": 1}))
    for i in items:
        i["_id"] = str(i["_id"])
    return {"products": items}

@app.get("/recommend/{product_id}")
def recommend(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return {"error": "Product not found"}

    idx = df[df["_id"] == product_id].index[0]
    distances, indices = model.kneighbors([df.iloc[idx][["price", "rating", "category_code"]]])
    recs = df.iloc[indices[0]].to_dict(orient="records")
    return {"recommendations": recs}
