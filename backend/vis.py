import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Load your products.csv
data = pd.read_csv("products.csv").dropna(subset=["price", "rating", "category"])
data.reset_index(drop=True, inplace=True)

# Encode category
enc = OneHotEncoder(sparse_output=False)
category_encoded = enc.fit_transform(data[["category"]])
category_df = pd.DataFrame(category_encoded, columns=enc.get_feature_names_out(["category"]))
data = pd.concat([data, category_df], axis=1)

# Prepare features
X = pd.concat([data[["price", "rating"]], category_df], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y = range(len(X))

# Train a small RandomForest with one tree for visualization
rf = RandomForestClassifier(n_estimators=1, random_state=42, max_depth=4)
rf.fit(X_scaled, y)

# Extract and plot the tree
tree = rf.estimators_[0]
plt.figure(figsize=(24, 12))
plot_tree(tree, feature_names=X.columns, filled=True, rounded=True, fontsize=8)
plt.title("Example of a Single Decision Tree from Random Forest", fontsize=16)
plt.show()
