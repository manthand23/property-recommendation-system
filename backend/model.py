import json
import numpy as np
from xgboost import XGBRegressor
from pathlib import Path
from utils import extract_features

WEIGHTS_PATH = Path("trained_weights.json")
MODEL_PATH = Path("xgb_model.json")

DEFAULT_WEIGHTS = {
    "gla_diff_norm": -1.0,
    "lot_size_diff_norm": -0.5,
    "bedroom_diff": -0.5,
    "bath_diff": -0.7,
    "age_diff_norm": -0.4,
    "sale_date_diff_years": -0.6,
    "geo_distance_km": -0.4,
    "same_structure_type": 0.5,
    "same_style": 0.4,
    "same_condition": 0.4,
    "same_basement_finish": 0.2
}

# Load weights or use default
if WEIGHTS_PATH.exists():
    with WEIGHTS_PATH.open("r") as f:
        weights = json.load(f)
else:
    weights = DEFAULT_WEIGHTS

# Optionally load trained XGBoost model
if MODEL_PATH.exists():
    xgb_model = XGBRegressor()
    xgb_model.load_model(str(MODEL_PATH))
else:
    xgb_model = None

def score_candidate(features: dict):
    explanation = {}
    weighted_sum = 0
    has_nan = False

    for key, value in features.items():
        w = weights.get(key, 0.0)
        explanation[key] = value
        if value is None or isinstance(value, float) and np.isnan(value):
            has_nan = True
            continue
        weighted_sum += w * value

    # Smoothed scoring function
    score = 1 / (1 + abs(weighted_sum))

    # Try ML fallback if all features are present
    if xgb_model and not has_nan:
        try:
            feature_order = list(DEFAULT_WEIGHTS.keys())
            x_values = np.array([[features.get(k, np.nan) for k in feature_order]])
            score = float(xgb_model.predict(x_values)[0])
        except Exception as e:
            print("ML fallback error, using linear scoring:", e)

    return {"score": score, "explanation": explanation}
