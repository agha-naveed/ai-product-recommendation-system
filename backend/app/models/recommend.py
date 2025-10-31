# backend/app/models/recommend.py
import joblib
import numpy as np

model = joblib.load("app/models/model.pkl")

def recommend_product(price: float):
    pred = model.predict(np.array([[price]]))
    return int(pred[0])
