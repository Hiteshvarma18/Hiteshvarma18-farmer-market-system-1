import joblib
import numpy as np
from datetime import datetime

model = joblib.load("ai_model/model.pkl")
crop_encoder = joblib.load("ai_model/crop_encoder.pkl")
market_encoder = joblib.load("ai_model/market_encoder.pkl")

def predict_price(crop, market, future_days):

    # encode inputs
    crop_encoded = crop_encoder.transform([crop])[0]
    market_encoded = market_encoder.transform([market])[0]

    # simple time reference
    base_days = 0
    days = base_days + future_days

    X = np.array([[days, crop_encoded, market_encoded]])

    result = model.predict(X)

    return float(result[0])