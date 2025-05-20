# Property Recommendation System

This full-stack project is a property comp recommender that helps real estate professionals and appraisers find the top 3 most comparable properties (comps) based on a given subject property. It uses a backend scoring model powered by XGBoost and a user-friendly React frontend.

---

1. How It Works
---

1. Scoring Engine (Backend)
- Accepts a subject property address and looks it up in `appraisals_dataset.json`
- Extracts features and scores each comp using:
  - Geographic distance
  - Bedroom/Bath/GLA differences
  - Structural matches (style, condition, basement)
- Uses an XGBoost model trained on feedback data to assign weights dynamically
- Returns the top 3 comps with score + breakdown explanation

2. Web App (Frontend)
- Allows user to enter subject property details (address must match dataset)
- Sends API request to `/recommend-from-dataset`
- Displays the 3 highest scoring comps with a feature-by-feature breakdown
- Accepts user feedback on comp quality (score 1–5), retrains after every 10 feedbacks
