import joblib

def load_model():
    return joblib.load("models/energy_model.pkl")  # Make sure this exists

def predict(model, X):
    return model.predict(X)
