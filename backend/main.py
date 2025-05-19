from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import RecommendationRequest, CompExplanation, FeedbackEntry
from model import extract_features, score_candidate
import json
from pathlib import Path
from datetime import datetime
import shutil
import subprocess
from fuzzywuzzy import process
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FEEDBACK_FILE = Path("feedback_log.json")
RETRAIN_LOG = Path("retrain_log.txt")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend", response_model=list[CompExplanation])
def recommend_comps(payload: RecommendationRequest):
    subject = payload.subject.dict()
    candidates = payload.candidates

    results = []
    for c in candidates:
        c_dict = c.dict()
        features = extract_features(subject, c_dict)
        scored = score_candidate(features)
        results.append({
            "id": c_dict["id"],
            "address": c_dict["address"],
            "score": scored["score"],
            "explanation": scored["explanation"]
        })

    return sorted(results, key=lambda x: x["score"])[:3]

@app.post("/feedback")
def collect_feedback(entry: FeedbackEntry):
    entry_dict = entry.dict()
    existing = []

    if FEEDBACK_FILE.exists():
        with FEEDBACK_FILE.open("r") as f:
            existing = json.load(f)

    existing.append(entry_dict)

    with FEEDBACK_FILE.open("w") as f:
        json.dump(existing, f, indent=2)

    if len(existing) % 10 == 0:
        try:
            subprocess.run(["python", "train_weights.py"], check=True)
            with RETRAIN_LOG.open("a") as log:
                log.write(f"[{datetime.now()}] Retrained after {len(existing)} feedbacks.\n")
        except subprocess.CalledProcessError:
            return {"message": "Feedback recorded. Retraining failed."}

    return {"message": "Feedback recorded."}

@app.post("/retrain")
def retrain_weights():
    try:
        subprocess.run(["python", "train_weights.py"], check=True)
        return {"message": "Retrained and updated weights."}
    except subprocess.CalledProcessError:
        return {"error": "Retraining failed."}

@app.get("/backups")
def list_backups():
    return sorted([f.name for f in Path("weights_backup").glob("weights_*.json")])

@app.post("/rollback")
def rollback_to_version(filename: str):
    path = Path("weights_backup") / filename
    if not path.exists():
        return {"error": "Backup not found."}
    shutil.copyfile(path, "trained_weights.json")
    return {"message": f"Restored {filename}"}

@app.post("/recommend-from-dataset")
def recommend_from_dataset(identifier: dict):
    dataset_path = Path("data/appraisals_dataset.json")
    if not dataset_path.exists():
        return {"error": "Dataset not found."}

    with dataset_path.open("r") as f:
        data = json.load(f)

    selected_appraisal = None

    if "property_id" in identifier:
        for appraisal in data["appraisals"]:
            if appraisal["subject"]["id"] == identifier["property_id"]:
                selected_appraisal = appraisal
                break
    elif "address" in identifier:
        all_subjects = {a["subject"]["address"]: a for a in data["appraisals"]}
        match, _ = process.extractOne(identifier["address"], list(all_subjects.keys()))
        selected_appraisal = all_subjects.get(match)

    if not selected_appraisal:
        return {"error": "Subject property not found."}

    subject = selected_appraisal["subject"]
    candidates = selected_appraisal["properties"]

    def clean_explanation(expl):
        return {
            k: (v if isinstance(v, (int, float)) and not math.isnan(v) else 0.0)
            for k, v in expl.items()
        }

    results = []
    for c in candidates:
        features = extract_features(subject, c)
        scored = score_candidate(features)
        results.append({
            "id": c.get("id", ""),
            "address": c.get("address", "Unknown"),
            "score": scored["score"] if not math.isnan(scored["score"]) else 0.0,
            "explanation": clean_explanation(scored["explanation"])
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:3]
