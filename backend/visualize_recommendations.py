import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
products = list(db["products"].find({}, {"_id": 0}))

# Convert to DataFrame
df = pd.DataFrame(products)

# Encode categories as numbers
le = LabelEncoder()
df["category_encoded"] = le.fit_transform(df["category"])

# Select numeric features
X = df[["price", "rating", "category_encoded"]]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA to reduce dimensions to 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["x"] = X_pca[:, 0]
df["y"] = X_pca[:, 1]

# Plot
plt.figure(figsize=(10, 7))
plt.scatter(df["x"], df["y"], c=df["category_encoded"], cmap="tab10", s=40, alpha=0.8)
plt.title("Product Similarity Graph (2D PCA)")
plt.xlabel("PCA Feature 1")
plt.ylabel("PCA Feature 2")

# Label some points for clarity
for i in range(0, len(df), max(1, len(df)//40)):  # label ~40 points
    plt.text(df["x"].iloc[i], df["y"].iloc[i], df["title"].iloc[i][:15], fontsize=7)

plt.colorbar(label="Category")
plt.show()
