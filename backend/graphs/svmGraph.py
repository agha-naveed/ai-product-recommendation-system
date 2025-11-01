import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.svm import SVC

# Load data
data = pd.read_csv("products.csv").dropna(subset=["price", "rating", "category"])
data.reset_index(drop=True, inplace=True)

# Encode category
enc = OneHotEncoder(sparse_output=False)
category_encoded = enc.fit_transform(data[["category"]])
category_df = pd.DataFrame(category_encoded, columns=enc.get_feature_names_out(["category"]))
X = pd.concat([data[["price", "rating"]], category_df], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Label encode categories (for visualization)
label_enc = LabelEncoder()
y = label_enc.fit_transform(data["category"])

# Train SVM using only price and rating (for graph simplicity)
svm = SVC(kernel='rbf', gamma=0.5, C=1)
svm.fit(X_scaled[:, :2], y)

# Create a mesh grid
x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                     np.linspace(y_min, y_max, 300))

# Predict each point on the grid
Z = svm.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# --- Select a sample product (for visualization) ---
sample_idx = 50  # change this number to test another product
sample_point = X_scaled[sample_idx]

# Plot decision boundaries
plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors='k')
plt.scatter(sample_point[0], sample_point[1], c='red', marker='*', s=200, label='Selected Product')

plt.xlabel("Price (scaled)")
plt.ylabel("Rating (scaled)")
plt.title("SVM Decision Boundary for Product Categories")
plt.legend()
plt.colorbar(label="Category (numeric)")
plt.show()
