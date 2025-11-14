Credit Card Fraud Detection System (XGBoost + FastAPI + Analytics UI)

This project implements a production-grade credit card fraud detection system using:

XGBoost for classification

FastAPI backend

HTML/CSS/JS interactive frontend

Real-time analytics panel

Single prediction + Bulk CSV prediction

Docker-ready deployment

The system is designed exactly like enterprise fraud engines — fast, stable, and optimized for imbalanced datasets.

📌 1. Project Overview

Credit card fraud is rare (~0.17% of all transactions).
This project focuses on detecting these extremely rare anomalies using machine learning.

The pipeline includes:

Data preprocessing

PCA-based anonymized features (V1–V28)

Imbalance-aware XGBoost model

Fast inference API

Modern analytics dashboard

Bulk CSV fraud scoring

📌 2. Dataset Explanation (Very Important)

We use the well-known Kaggle European Credit Card Fraud Dataset (2013).
It contains:

284,807 total transactions

492 fraud transactions

Fraud ratio: 0.172%

⚠ Why are fraud results often “0” for custom inputs?

Because:

(1) Features V1–V28 are PCA components

These are not real-world values like “merchant name” or “location”.
They were converted using Principal Component Analysis to protect privacy.

➡ Meaning:
You cannot guess or manually generate values that correspond to real fraud patterns.

Only actual PCA-transformed vectors will trigger fraud.

(2) Fraud is extremely rare

Even in training, 99.83% of samples are NOT fraud.

So the model only predicts fraud when:

PCA components match real fraud patterns

Amount/time patterns match anomalies

Behavior aligns with known fraud signatures

Manually typing numbers rarely matches real PCA structure → prediction remains low.

(3) Fraud detection is anomaly-based

Increasing “Amount” or “Time” does NOT necessarily convert a sample into fraud.

Fraud depends on hidden PCA relationships, not isolated values.

📌 3. Model Training Details

We train XGBoost with class imbalance correction.

Key techniques used:

✔ scale_pos_weight = (negatives / positives)

To boost fraud recall.

✔ No scaling of inputs

PCA features are already normalized; scaling weakens fraud signal.

✔ Carefully tuned threshold:
Fraud if probability ≥ 0.20


Gives the best recall/precision balance.

📌 4. API Structure
POST /predict

Predicts fraud for a single JSON payload:

{
  "features": {
    "Time": 406,
    "V1": -1.23,
    ...
    "V28": 0.15,
    "Amount": 181
  }
}


Returns:

{
  "prediction": 0,
  "probability": 0.0492,
  "top_features": [
    {"feature": "Time", "value": 406},
    {"feature": "Amount", "value": 181},
    {"feature": "V11", "value": -3.22}
  ]
}

POST /bulk_predict

Upload a CSV with columns:

Time,V1,V2,...,V28,Amount


Returns:

Fraud prediction for every row

Downloadable results CSV

Analytics panel auto-updates

📌 5. Frontend UI Features

The integrated UI provides:

✔ Single Transaction Prediction

Enter features

Run analysis

Animated fraud probability circle

Top contributing features

Result summary

✔ Bulk CSV Upload

Upload .csv

Get table of fraud predictions

Download CSV of results

✔ Session Analytics Panel (Floating)

Fraud vs. non-fraud donut chart

Probability trendline

Total predictions in this session

Fraud percentage

Auto-updates after every prediction

📌 6. Project Structure
credit-card-fraud-detection/
│
├── app/
│   └── main.py               # FastAPI backend
│
├── src/
│   ├── train.py              # Training script
│   ├── predict.py            # Prediction helpers
│   └── preprocess.py
│
├── frontend/
│   └── index.html            # Entire user interface
│
├── model/
│   ├── model.pkl             # XGBoost model
│   └── scaler.pkl            # (Unused in final version)
│
├── data/
│   └── creditcard.csv        # Dataset
│
├── requirements.txt
├── Dockerfile
├── notebook/
│   └── notebook.ipynb
└── README.md                 # ← YOU ARE HERE

📌 7. How to Run Locally
1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. Open browser
http://localhost:8000


Done.

📌 8. Docker Deployment

Build image:

docker build -t fraud-detector .


Run container:

docker run -p 8000:8000 fraud-detector


Open:

http://localhost:8000

📌 9. Limitations (Include This — Very Important)

PCA features cannot be meaningfully guessed manually.

Fraud patterns are hidden in PCA structure, not in single fields.

The dataset is extremely imbalanced (0.17% fraud).

Model only detects fraud when PCA signature matches actual fraud.

Manual or random inputs almost never match real PCA fraud vectors.

Because of this:

Bulk test of real fraud rows works (shows fraud)

Manual input generally shows safe

This is expected and correct model behavior.

📌 10. Conclusion

This system is a full end-to-end, production-style fraud detection pipeline:

Reliable

Fast

Visually rich

Realistic

Properly handles imbalanced classification

Matches industry patterns (PCA-based fraud scoring)

The model behaves exactly like real enterprise fraud engines:
Predicts fraud only when the internal PCA pattern matches real fraud vectors.