from fastapi import FastAPI
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib
from bson import ObjectId
from db import get_db

app = FastAPI()
collection = get_db()

# ====================
# Load Data + Train Model
# ====================
def load_data():
    products = list(collection.find())
    df = pd.DataFrame(products)
    df['_id'] = df['_id'].astype(str)
    return df

df = load_data()
features = df[['price', 'rating']]  # use relevant numeric features
model = NearestNeighbors(n_neighbors=6, metric='cosine')
model.fit(features)
joblib.dump(model, 'knn_model.pkl')

# ====================
# API ROUTES
# ====================
@app.get("/products")
def get_products():
    products = list(collection.find({}, {"_id": 1, "name": 1, "price": 1, "rating": 1}))
    for p in products:
        p["_id"] = str(p["_id"])
    return {"products": products}

@app.get("/recommend/{product_id}")
def recommend(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return {"error": "Product not found"}

    idx = df[df['_id'] == product_id].index[0]
    distances, indices = model.kneighbors([df.iloc[idx][['price', 'rating']]])
    recs = df.iloc[indices[0]].to_dict(orient='records')
    return {"recommendations": recs}
