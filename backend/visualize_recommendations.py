from pymongo import MongoClient
from bson import ObjectId
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
products_col = db["products"]
users_col = db["users"]

def build_feature_matrix():
    products = list(products_col.find({}, {"_id": 1, "category": 1, "price": 1, "rating": 1}))
    df = pd.DataFrame(products)

    # Encode categories
    le = LabelEncoder()
    df["category_encoded"] = le.fit_transform(df["category"].astype(str))

    # Scale features
    X = df[["price", "rating", "category_encoded"]].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return df, X_scaled, le

def plot_user(user_id):
    df, X_scaled, le = build_feature_matrix()
    user = users_col.find_one({"user_id": user_id})

    if not user or "liked_products" not in user or len(user["liked_products"]) == 0:
        print("⚠️ User has no liked products.")
        return

    liked_ids = [ObjectId(pid) for pid in user["liked_products"] if ObjectId.is_valid(pid)]
    liked_mask = df["_id"].isin(liked_ids)

    # Apply KNN
    knn = NearestNeighbors(n_neighbors=6)
    knn.fit(X_scaled)

    liked_indices = df.index[liked_mask].tolist()
    rec_indices = set()
    for idx in liked_indices:
        _, indices = knn.kneighbors([X_scaled[idx]])
        rec_indices.update(indices[0])

    rec_indices = list(rec_indices)

    # PCA for 2D visualization
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(X_scaled)
    df["x"], df["y"] = reduced[:, 0], reduced[:, 1]

    df["color"] = "gray"
    df.loc[liked_mask, "color"] = "green"
    df.loc[rec_indices, "color"] = "red"

    # Visualization
    plt.figure(figsize=(10, 8))
    for color, label in [("green", "Liked"), ("red", "Recommended"), ("gray", "Other")]:
        subset = df[df["color"] == color]
        plt.scatter(subset["x"], subset["y"], c=color, label=label, alpha=0.7, s=80, edgecolors='k')

    plt.title(f"Personalized Recommendation Graph for {user_id}")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Optional: Show categories for context
    for _, row in df[df["color"] != "gray"].iterrows():
        plt.text(row["x"] + 0.05, row["y"], row["category"], fontsize=8)

    plt.show()

# Run
plot_user("user123")
