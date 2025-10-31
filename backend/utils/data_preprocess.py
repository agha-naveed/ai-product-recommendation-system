# backend/utils/data_preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(data):
    df = pd.DataFrame(data)
    df['category'] = LabelEncoder().fit_transform(df['category'])
    df['rating'] = df['rating'].fillna(df['rating'].mean())
    df['price'] = df['price'].fillna(df['price'].mean())
    return df
