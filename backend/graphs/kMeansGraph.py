import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib.colors import ListedColormap

# Load data
data = pd.read_csv("products.csv").dropna(subset=["price", "rating"])
data.reset_index(drop=True, inplace=True)

# Only use price & rating for visualization
X = data[["price", "rating"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means (2D)
kmeans = KMeans(n_clusters=6, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
data["cluster"] = clusters

# Pick a product to highlight
sample_idx = 50  # Change this to any index
sample_point = X_scaled[sample_idx]

# Mesh grid for contours
x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                     np.linspace(y_min, y_max, 400))

# Predict for each grid point
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot
plt.figure(figsize=(10, 6))
cmap = ListedColormap(plt.cm.tab10.colors[:len(np.unique(clusters))])
plt.contourf(xx, yy, Z, alpha=0.2, cmap=cmap)

# Scatter actual data
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap=cmap,
            edgecolors='k', s=50, alpha=0.8)

# Cluster centers
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c='black', marker='X', s=200, label='Cluster Centers')

# Selected product
plt.scatter(sample_point[0], sample_point[1], c='red', marker='*', s=200, label='Selected Product')

plt.title("K-Means Clustering with Decision Boundaries (Price vs Rating)")
plt.xlabel("Price (scaled)")
plt.ylabel("Rating (scaled)")
plt.legend()
plt.show()
