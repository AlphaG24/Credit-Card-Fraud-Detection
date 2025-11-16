# Credit Card Fraud Detection System

Real-time transaction scoring service that flags high-risk credit card transactions using a PCA-preserved XGBoost classifier. Use-case: integrate with merchant transaction pipelines to block or review suspicious payments.

Production Demo: https://credit-card-fraud-detection-1nll.onrender.com

---

## 📌 1. Project Overview

Credit card fraud occurs in only **0.17%** of transactions.  
This project implements a complete, production-grade fraud detection system with:

- XGBoost classifier optimized for extreme class imbalance  
- PCA-transformed anonymized features (V1–V28)  
- Threshold-tuned decision logic  
- FastAPI backend  
- Frontend for single & bulk predictions  
- Docker + Render deployment  

The system is **fast, stable, and realistic**, matching enterprise fraud engines.

---

## 📌 2. Dataset (Training Only — Not Required for Deployment)

Dataset used:

**European Credit Card Fraud Dataset (Kaggle)**  
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

**Dataset facts:**

- 284,807 rows  
- Target distribution: 284,807 rows, 492 fraud (0.172%).
- Amount distribution: heavy right skew — median < mean; frauds skew to high amounts but not exclusively.
- PCA features: V1..V28 are anonymized; top contributing features found via model feature importance: V11, V2, V1 (see notebook).
- Missing data: none (dataset complete).
- Features: Time, Amount, V1–V28 (PCA components)

“EDA is fully documented in notebook/notebook.ipynb.”

The dataset is **NOT included** in the repository because:

- It is large  
- Not required for deployment  
- Model is already pre-trained (`model/model.pkl`)  

To retrain, manually place:

data/creditcard.csv

yaml
Copy code

---

## 📌 3. Why Manual Inputs Usually Show “NOT FRAUD”

This behavior is **expected** and correct:

- V1–V28 are **PCA components** → you cannot guess real values by hand  
- Fraud signatures appear only when **multi-dimensional PCA patterns align**  
- Changing Amount or Time alone rarely impacts classification  
- Real fraud rows from the test set *will* generate fraud predictions  

This matches behavior of real enterprise fraud detection systems.

---

## 📌 4. Model Training Summary

This project uses **XGBoost** because it performs best for imbalanced binary classification.

Key techniques:

- `scale_pos_weight = negatives / positives`  
- No scaling (PCA values are already normalized)  
- Decision threshold tuned at **0.20** for optimal fraud recall  

Training command:

python src/train.py --data data/creditcard.csv --out_model model/model.pkl

yaml
Copy code

---

## 📌 5. Model Comparison (Why XGBoost Was Selected)

Multiple algorithms were tested:

| Model                | Recall (Fraud) | Precision (Fraud) | F1 Score | ROC-AUC | Notes |
|---------------------|----------------|-------------------|---------|---------|-------|
| Logistic Regression | Low (~0.50)    | Very low          | Weak    | 0.94    | Too simple for PCA fraud patterns |
| Random Forest       | Medium (~0.75) | Medium            | Decent  | 0.96    | Slower inference |
| **XGBoost (Chosen)**| **~0.86**      | **~0.70**         | **Best**| **0.978** | Best balance of recall, precision, speed |

**Reason for choosing XGBoost:**
- Best fraud recall  
- Best F1 score  
- Most stable on PCA-transformed data  
- Fastest inference for production  

All models were evaluated using the same train/test split and stratified sampling for fairness.

---

## 📌 6. API Endpoints

### ✔ `POST /predict` (Single Transaction)

**Request:**
```json
{
  "features": {
    "Time": 41194,
    "V1": -7.89,
    "V2": 5.38,
    "V3": -4.09,
    "...": 0,
    "V28": 0.21,
    "Amount": 1.52
  }
}
Response:

json
Copy code
{
  "prediction": 0,
  "probability": 0.0065,
  "top_features": [
    {"feature": "Time", "value": 41194},
    {"feature": "Amount", "value": 1.52},
    {"feature": "V1", "value": -7.89}
  ]
}
✔ POST /bulk_predict (CSV Upload)
Upload a CSV with:

css
Copy code
Time, V1, V2, ..., V28, Amount
Returns:

Fraud predictions per row

Probability scores

Downloadable CSV

Frontend analytics auto-updates

✔ GET /download_last_csv
Downloads the latest processed CSV.

✔ GET /health
Used for monitoring and Render uptime checks.

📌 7. Project Structure
css
Copy code
credit-card-fraud-detection/
│
├── app/
│   └── main.py
│
├── src/
│   ├── train.py
│   ├── predict.py
│   └── preprocess.py
│
├── frontend/
│   └── index.html
│
├── model/
│   └── model.pkl
│
├── data/
│   └── .gitkeep
│
├── requirements.txt
├── Dockerfile
├── Procfile
├── notebook/
│   └── notebook.ipynb
└── README.md

📌 8. Run Locally

Create virtual environment:

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
Install dependencies:

nginx
Copy code
pip install -r requirements.txt
Start server:

nginx
Copy code
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Open browser:

arduino
Copy code
http://localhost:8000

📌 9. Docker Deployment

Build:

nginx
Copy code
docker build -t fraud-detector .
Run:

arduino
Copy code
docker run -p 8000:8000 fraud-detector

📌 10. Render Deployment (Production)

Already deployed at:

https://credit-card-fraud-detection-1nll.onrender.com

Render settings:

Environment: Docker

Port: Auto-detected (8000)

Root directory: /

No dataset required for deployment.

📌 11. Limitations

Manual input almost never matches real PCA fraud patterns

PCA components limit interpretability

Threshold may need tuning for different datasets

Fraud detection inherently suffers from extreme imbalance

📌 12. Evaluation & Reproducibility

A separate file EVALUATION.md includes:

Metrics

Model comparison

Threshold justification

Steps to retrain

The notebook can be executed end-to-end without errors after placing the dataset into data/creditcard.csv.

📌 13. Conclusion

This project demonstrates:

Enterprise-like fraud detection pipeline

High fraud recall with XGBoost

Fully working API + UI

Bulk scoring + analytics

Production deployment on Render

Reproducible training workflow

A complete, end-to-end, production-ready fraud detection system.