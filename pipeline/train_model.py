import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from utils.preprocessing import preprocess_data

df = pd.read_csv("data/sample_energy.csv", parse_dates=["Timestamp"])
df = preprocess_data(df)

X = df[["hour", "dayofweek"]]
y = df["EnergyConsumption"]

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "models/forecast_model.pkl")
print("✅ Model saved at models/forecast_model.pkl")
