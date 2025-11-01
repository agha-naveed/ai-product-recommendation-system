# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.cluster import KMeans

# ===============================
#  APP INITIALIZATION
# ===============================
app = FastAPI(title="AI Product Recommendation API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
#  LOAD DATA & TRAIN MODELS
# ===============================
data = pd.read_csv("products.csv").dropna(subset=["price", "rating", "category"])
data.reset_index(drop=True, inplace=True)

# --- Encode category ---
enc = OneHotEncoder(sparse_output=False)
category_encoded = enc.fit_transform(data[["category"]])
category_df = pd.DataFrame(category_encoded, columns=enc.get_feature_names_out(["category"]))
data = pd.concat([data, category_df], axis=1)

# --- Features ---
X = pd.concat([data[["price", "rating"]], category_df], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y = np.arange(len(X))

# --- Train Models ---
knn = KNeighborsClassifier(n_neighbors=5)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
logr = LogisticRegression(max_iter=1000)
svm = SVC(probability=True, kernel="rbf")
kmeans = KMeans(n_clusters=6, random_state=42)

knn.fit(X_scaled, y)
rf.fit(X_scaled, y)
logr.fit(X_scaled, y)
svm.fit(X_scaled, y)
data["cluster"] = kmeans.fit_predict(X_scaled)

# ===============================
#  REQUEST MODEL
# ===============================
class ProductInput(BaseModel):
    price: float
    rating: float
    category: str

# ===============================
#  ROUTES
# ===============================

@app.get("/")
async def root():
    return {"message": "AI Product Recommender API is running 🚀"}


@app.get("/products")
async def get_products():
    """Return all products"""
    return data.to_dict(orient="records")


@app.post("/recommend")
async def recommend(item: ProductInput):
    """Hybrid AI-based recommendation with category filtering"""
    price = item.price
    rating = item.rating
    category = item.category

    # Filter same-category data
    same_cat_data = data[data["category"].str.lower() == category.lower()]
    if same_cat_data.empty:
        same_cat_data = data  # fallback

    # Encode within subset
    X_sub = pd.concat(
        [same_cat_data[["price", "rating"]], same_cat_data[enc.get_feature_names_out(["category"])]],
        axis=1
    )
    X_sub_scaled = scaler.transform(X_sub)

    # Input vector encoding
    cat_vector = np.zeros(len(enc.get_feature_names_out(["category"])))
    if category in enc.categories_[0]:
        idx = list(enc.categories_[0]).index(category)
        cat_vector[idx] = 1
    input_vector = np.concatenate(([price, rating], cat_vector)).reshape(1, -1)
    input_scaled = scaler.transform(input_vector)

    # ===============================
    #  MODEL PREDICTIONS
    # ===============================

    # 1️⃣ KNN
    knn_neighbors = knn.kneighbors(input_scaled, return_distance=False)[0]
    knn_score = {i: 1 for i in knn_neighbors if i in same_cat_data.index}

    # 2️⃣ Random Forest
    rf_probs = rf.predict_proba(input_scaled)[0]
    rf_top = np.argsort(rf_probs)[-5:]
    rf_score = {i: 1 for i in rf_top if i in same_cat_data.index}

    # 3️⃣ Logistic Regression
    lr_probs = logr.predict_proba(input_scaled)[0]
    lr_top = np.argsort(lr_probs)[-5:]
    lr_score = {i: 1 for i in lr_top if i in same_cat_data.index}

    # 4️⃣ SVM
    svm_probs = svm.predict_proba(input_scaled)[0]
    svm_top = np.argsort(svm_probs)[-5:]
    svm_score = {i: 1 for i in svm_top if i in same_cat_data.index}

    # 5️⃣ K-Means
    cluster_label = kmeans.predict(input_scaled)[0]
    cluster_items = same_cat_data[same_cat_data["cluster"] == cluster_label].index[:5]
    cluster_score = {i: 1 for i in cluster_items}

    # ===============================
    #  COMBINE RESULTS (Weighted)
    # ===============================
    combined_scores = {}
    models = [
        (knn_score, 0.3),
        (rf_score, 0.25),
        (lr_score, 0.2),
        (svm_score, 0.15),
        (cluster_score, 0.1),
    ]

    for model_scores, weight in models:
        for i, score in model_scores.items():
            combined_scores[i] = combined_scores.get(i, 0) + score * weight

    # ===============================
    #  FINAL TOP RECOMMENDATIONS
    # ===============================
    if not combined_scores:
        recs = same_cat_data.sample(min(5, len(same_cat_data))).to_dict(orient="records")
    else:
        top_indexes = sorted(combined_scores, key=combined_scores.get, reverse=True)[:5]
        recs = data.loc[top_indexes].to_dict(orient="records")

    return recs
