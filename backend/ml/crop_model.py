import numpy as np
import pickle, os, csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

MODEL_PATH  = "ml/crop_model.pkl"
SCALER_PATH = "ml/crop_scaler.pkl"
ENCODER_PATH = "ml/crop_encoder.pkl"
DATA_PATH   = "ml/crop_data.csv"

def load_csv_data():
    X, y = [], []
    with open(DATA_PATH, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([
                float(row['N']), float(row['P']), float(row['K']),
                float(row['temperature']), float(row['humidity']),
                float(row['ph']), float(row['rainfall'])
            ])
            y.append(row['label'])
    return np.array(X), np.array(y)

def _train_and_save():
    X, y = load_csv_data()
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_sc, y_enc)
    os.makedirs("ml", exist_ok=True)
    with open(MODEL_PATH,   "wb") as f: pickle.dump(model,  f)
    with open(SCALER_PATH,  "wb") as f: pickle.dump(scaler, f)
    with open(ENCODER_PATH, "wb") as f: pickle.dump(le,     f)
    print(f"Model trained on {len(X)} records, {len(le.classes_)} crops!")
    return model, scaler, le

def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(ENCODER_PATH):
        with open(MODEL_PATH,   "rb") as f: model  = pickle.load(f)
        with open(SCALER_PATH,  "rb") as f: scaler = pickle.load(f)
        with open(ENCODER_PATH, "rb") as f: le     = pickle.load(f)
    else:
        model, scaler, le = _train_and_save()
    return model, scaler, le

def recommend_crops(N, P, K, temperature, humidity, ph, rainfall, top_n=3):
    model, scaler, le = load_model()
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    features_sc = scaler.transform(features)
    proba = model.predict_proba(features_sc)[0]
    top_indices = np.argsort(proba)[::-1][:top_n]
    results = []
    for idx in top_indices:
        crop_name = le.classes_[idx]
        results.append({
            "crop":        crop_name.capitalize(),
            "confidence":  round(float(proba[idx]) * 100, 1),
            "suitability": "High" if proba[idx] > 0.5 else "Moderate" if proba[idx] > 0.2 else "Low"
        })
    return results