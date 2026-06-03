import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("../data/mandi.csv")

df["date"] = pd.to_datetime(df["date"])

df["days"] = (df["date"] - df["date"].min()).dt.days

# ---------------------------
# ENCODING (NEW UPGRADE)
# ---------------------------
crop_encoder = LabelEncoder()
market_encoder = LabelEncoder()

df["crop_encoded"] = crop_encoder.fit_transform(df["crop"])
df["market_encoded"] = market_encoder.fit_transform(df["market"])

# FEATURES
X = df[["days", "crop_encoded", "market_encoded"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

# SAVE EVERYTHING
joblib.dump(model, "model.pkl")
joblib.dump(crop_encoder, "crop_encoder.pkl")
joblib.dump(market_encoder, "market_encoder.pkl")

print("AI Model Training Complete")