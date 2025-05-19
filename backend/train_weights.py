import json
import numpy as np
from xgboost import XGBRegressor
from pathlib import Path
from utils import extract_features

# Paths
FEEDBACK_PATH = Path("feedback_log.json")
MODEL_PATH = Path("xgb_model.json")
WEIGHTS_PATH = Path("trained_weights.json")

# Load feedback log
with FEEDBACK_PATH.open("r") as f:
    feedback_data = json.load(f)

X = []
y = []

# Generate training samples
for entry in feedback_data:
    subject = entry.get("subject", {})
    comp_id = entry.get("comp_id")
    score = entry.get("feedback_score")

    # Load appraisal dataset to find the candidate with the matching ID
    dataset_path = Path("data/appraisals_dataset.json")
    with dataset_path.open("r") as f:
        full_data = json.load(f)

    found = False
    for appraisal in full_data["appraisals"]:
        for prop in appraisal["properties"]:
            if str(prop.get("id")) == str(comp_id):
                features = extract_features(subject, prop)
                X.append([features.get(k, np.nan) for k in sorted(features)])
                y.append(score)
                found = True
                break
        if found:
            break

# Train model if we have enough data
if len(X) >= 10:
    X = np.array(X)
    y = np.array(y)

    model = XGBRegressor()
    model.fit(X, y)
    model.save_model(MODEL_PATH)

    # Also update the linear weights as backup
    avg_weights = np.mean(X, axis=0)
    feature_keys = sorted(features.keys())
    trained_weights = dict(zip(feature_keys, avg_weights))
    with WEIGHTS_PATH.open("w") as f:
        json.dump(trained_weights, f, indent=2)

    print("Model retrained and saved.")
else:
    print("Not enough data to retrain model.")
