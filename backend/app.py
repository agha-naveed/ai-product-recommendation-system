from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)
CORS(app)

# --- Load CSV ---
data = pd.read_csv("products.csv").dropna(subset=["price", "rating", "category"])
data.reset_index(drop=True, inplace=True)

# --- Encode categorical ---
le = LabelEncoder()
data["category"] = data["category"].astype(str)
data["category_code"] = le.fit_transform(data["category"])

# --- Features ---
X = data[["price", "rating", "category_code"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y = np.arange(len(X))

# --- Models ---
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

@app.route("/products", methods=["GET"])
def get_products():
    """Return all products"""
    return jsonify(data.to_dict(orient="records"))

@app.route("/recommend", methods=["POST"])
def recommend():
    """Weighted hybrid recommendation"""
    item = request.json
    price = item.get("price", 500)
    rating = item.get("rating", 3)
    category = str(item.get("category", "Electronics"))

    # Encode category
    if category in le.classes_:
        cat_code = le.transform([category])[0]
    else:
        cat_code = 0

    input_data = np.array([[price, rating, cat_code]])
    input_scaled = scaler.transform(input_data)

    # 1️⃣ KNN
    knn_neighbors = knn.kneighbors(input_scaled, return_distance=False)[0]
    knn_score = {i: 1 for i in knn_neighbors}

    # 2️⃣ Random Forest
    rf_probs = rf.predict_proba(input_scaled)[0]
    rf_top = np.argsort(rf_probs)[-5:]
    rf_score = {i: 1 for i in rf_top}

    # 3️⃣ Logistic Regression
    lr_probs = logr.predict_proba(input_scaled)[0]
    lr_top = np.argsort(lr_probs)[-5:]
    lr_score = {i: 1 for i in lr_top}

    # 4️⃣ SVM
    svm_probs = svm.predict_proba(input_scaled)[0]
    svm_top = np.argsort(svm_probs)[-5:]
    svm_score = {i: 1 for i in svm_top}

    # 5️⃣ KMeans cluster
    cluster_label = kmeans.predict(input_scaled)[0]
    cluster_items = data[data["cluster"] == cluster_label].index[:5]
    cluster_score = {i: 1 for i in cluster_items}

    # Combine with weights
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

    # Get top 5 recommendations
    top_indexes = sorted(combined_scores, key=combined_scores.get, reverse=True)[:5]
    recs = data.iloc[top_indexes].to_dict(orient="records")

    return jsonify(recs)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
