from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

client = MongoClient("mongodb://localhost:27017/")
db = client["recommender_db"]
collection = db["products"]

# Load data
products = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(products)

# Encode categories
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df[["category"]])
cat_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(["category"]))
df = pd.concat([df, cat_df], axis=1)

# Scale
features = ["price", "rating"] + list(cat_df.columns)
scaler = StandardScaler()
scaled = scaler.fit_transform(df[features])

# PCA
pca = PCA(n_components=2)
reduced = pca.fit_transform(scaled)
df["pca1"], df["pca2"] = reduced[:, 0], reduced[:, 1]

# Pick random product
idx = np.random.randint(0, len(df))
target = df.iloc[idx]
same_cat = df[df["category"] == target["category"]].reset_index(drop=True)

# KNN (same category)
model = NearestNeighbors(n_neighbors=min(6, len(same_cat)), metric="cosine")
X_same = scaled[df["category"] == target["category"]]
model.fit(X_same)
target_idx = same_cat[same_cat["title"] == target["title"]].index[0]
distances, indices = model.kneighbors([X_same[target_idx]])

# Plot
plt.figure(figsize=(8,6))
plt.scatter(same_cat["pca1"], same_cat["pca2"], c="gray", alpha=0.4)
plt.scatter(same_cat.iloc[target_idx]["pca1"], same_cat.iloc[target_idx]["pca2"],
            c="red", s=300, label="Target Product")
plt.scatter(same_cat.iloc[indices[0][1:]]["pca1"], same_cat.iloc[indices[0][1:]]["pca2"],
            c="orange", s=200, label="Recommended")
for i in indices[0][1:]:
    plt.text(same_cat["pca1"][i]+0.02, same_cat["pca2"][i], same_cat["title"][i][:15], fontsize=8)
plt.title(f"🧩 KNN Recommendations for '{target['title']}'")
plt.legend()
plt.show()

print(f"\n🎯 Target: {target['title']} ({target['category']})")
print("\nRecommended Products:")
for i in indices[0][1:]:
    print(f"→ {same_cat.iloc[i]['title']} | Price: {same_cat.iloc[i]['price']} | Rating: {same_cat.iloc[i]['rating']}")
