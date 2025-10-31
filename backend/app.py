# backend/app.py
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

kmeans = joblib.load('models/kmeans_model.pkl')
rf = joblib.load('models/random_forest.pkl')
knn = joblib.load('models/knn_model.pkl')
svm = joblib.load('models/svm_model.pkl')

data = pd.read_json('data/products.json')

@app.route('/recommend', methods=['POST'])
def recommend():
    product = request.json
    df = pd.DataFrame([product])

    # Predict cluster using multiple models
    cluster_kmeans = int(kmeans.predict(df[['price', 'rating', 'category']])[0])
    cluster_rf = int(rf.predict(df[['price', 'rating', 'category']])[0])
    cluster_knn = int(knn.predict(df[['price', 'rating', 'category']])[0])
    cluster_svm = int(svm.predict(df[['price', 'rating', 'category']])[0])

    # Combine results
    final_cluster = max(set([cluster_kmeans, cluster_rf, cluster_knn, cluster_svm]), key=[cluster_kmeans, cluster_rf, cluster_knn, cluster_svm].count)

    # Recommend products from that cluster
    recs = data[data['cluster'] == final_cluster].sample(5).to_dict(orient='records')
    return jsonify(recs)
