# backend/train_models.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib

data = pd.read_json('data/products.json')

X = data[['price', 'rating', 'category']]

# Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
data['cluster'] = kmeans.fit_predict(X)

# Train classifiers
rf = RandomForestClassifier()
rf.fit(X, data['cluster'])

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, data['cluster'])

svm = SVC()
svm.fit(X, data['cluster'])

# Save models
joblib.dump(kmeans, 'models/kmeans_model.pkl')
joblib.dump(rf, 'models/random_forest.pkl')
joblib.dump(knn, 'models/knn_model.pkl')
joblib.dump(svm, 'models/svm_model.pkl')
