# visualize_recommendations.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

# ======================================
# 1️⃣ LOAD PRODUCT DATA
# ======================================
# Example dataset (replace with MongoDB export or fakestoreapi data)
data = [
    {"name": "Laptop A", "category": "electronics", "price": 700, "rating": 4.5},
    {"name": "Laptop B", "category": "electronics", "price": 720, "rating": 4.4},
    {"name": "Phone X", "category": "electronics", "price": 400, "rating": 4.2},
    {"name": "T-Shirt Red", "category": "clothing", "price": 25, "rating": 4.1},
    {"name": "Jeans Blue", "category": "clothing", "price": 40, "rating": 4.3},
    {"name": "Gold Ring", "category": "jewelry", "price": 200, "rating": 4.8},
    {"name": "Necklace", "category": "jewelry", "price": 350, "rating": 4.7},
    {"name": "Shoes Black", "category": "clothing", "price": 60, "rating": 4.4},
    {"name": "Smart Watch", "category": "electronics", "price": 250, "rating": 4.6},
    {"name": "Earrings", "category": "jewelry", "price": 180, "rating": 4.5}
]
df = pd.DataFrame(data)

# ======================================
# 2️⃣ ENCODE CATEGORY (ONE-HOT)
# ======================================
encoder = OneHotEncoder(sparse_output=False)
encoded_cats = encoder.fit_transform(df[["category"]])
cat_df = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(["category"]))
df = pd.concat([df, cat_df], axis=1)

# ======================================
# 3️⃣ FEATURE SELECTION & SCALING
# ======================================
features = ["price", "rating"] + list(cat_df.columns)
X = df[features].values
scaler = StandardScaler()
scaled_X = scaler.fit_transform(X)

# ======================================
# 4️⃣ TRAIN KNN MODEL
# ======================================
model = NearestNeighbors(n_neighbors=6, metric="cosine")
model.fit(scaled_X)

# ======================================
# 5️⃣ PCA FOR VISUALIZATION
# ======================================
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_X)
df["pca1"] = pca_result[:, 0]
df["pca2"] = pca_result[:, 1]

# ======================================
# 6️⃣ VISUALIZE CLUSTERS BY CATEGORY
# ======================================
plt.figure(figsize=(8, 6))
scatter = plt.scatter(df["pca1"], df["pca2"],
                      c=pd.factorize(df["category"])[0],
                      cmap="viridis", s=120, alpha=0.8)
plt.title("🛍️ Product Clusters by Category", fontsize=14)
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.colorbar(scatter, label="Category")
for i, name in enumerate(df["name"]):
    plt.text(df["pca1"][i]+0.03, df["pca2"][i], name, fontsize=8)
plt.show()

# ======================================
# 7️⃣ PICK ONE PRODUCT & SHOW RECOMMENDATIONS
# ======================================
idx = np.random.randint(0, len(df))
distances, indices = model.kneighbors([scaled_X[idx]])

plt.figure(figsize=(8, 6))
plt.scatter(df["pca1"], df["pca2"], c="gray", alpha=0.3, s=100)
plt.scatter(df.iloc[idx]["pca1"], df.iloc[idx]["pca2"], color="red", s=300, label="Target Product")
plt.scatter(df.iloc[indices[0][1:]]["pca1"], df.iloc[indices[0][1:]]["pca2"],
            color="orange", s=200, label="Recommended Products")

for i in indices[0][1:]:
    plt.text(df["pca1"][i]+0.03, df["pca2"][i], df.iloc[i]["name"], fontsize=9)

plt.text(df["pca1"][idx]+0.03, df["pca2"][idx], df.iloc[idx]["name"], fontsize=10, fontweight="bold", color="red")
plt.legend()
plt.title("🎯 KNN Product Recommendations Visualization")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.show()

# ======================================
# 8️⃣ PRINT RECOMMENDATION RESULTS
# ======================================
print(f"\n🔍 Target Product: {df.iloc[idx]['name']} ({df.iloc[idx]['category']})")
print("Recommended Products:")
for i in indices[0][1:]:
    print(f" → {df.iloc[i]['name']} ({df.iloc[i]['category']})")
