# backend/app/models/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from app.db import products_collection

async def train_model():
    products = await products_collection.find().to_list(length=1000)
    if not products:
        print("⚠️ No data found in MongoDB. Fetch products first.")
        return

    df = pd.DataFrame(products)
    df = df.dropna(subset=["price"])

    # Simplified label: classify products as cheap (0) or expensive (1)
    median_price = df["price"].median()
    df["label"] = (df["price"] > median_price).astype(int)

    X = df[["price"]].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, "app/models/model.pkl")
    print("✅ Model trained and saved at app/models/model.pkl")
