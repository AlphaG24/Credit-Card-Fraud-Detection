📌 1. Project Overview

Credit card fraud is extremely rare (~0.17% of transactions).
This system is optimized for such imbalance using:

PCA-transformed anonymized features (V1–V28)

Proper scale_pos_weight tuning

Threshold-adjusted scoring

Fully integrated frontend for single + bulk predictions

The application is stable, fast, and deployable anywhere.

📌 2. Dataset (For Training Only — NOT Required for Deployment)

This system uses the Kaggle European Credit Card Fraud Dataset (2013):

📥 Download from here:
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Dataset facts:

Property	Value
Total rows	284,807
Fraud cases	492
Fraud percentage	0.172%
Features	Time, Amount, V1–V28 (PCA components)
❗ Important

The dataset is NOT included in the repo (too large & not required).

Render deployment does NOT require the dataset.

The model is already pre-trained into model/model.pkl.

Dataset is only needed if you want to retrain.

Place it here for training:

data/creditcard.csv

📌 3. Why Manual Inputs Often Show “Not Fraud”

This is expected and correct.

✔ PCA Components

V1–V28 are PCA-transformed numbers you cannot guess manually.

✔ Fraud patterns require multi-dimensional alignment

Changing “Amount” or “Time” alone does nothing.

✔ Fraud is extremely rare

Model fires only when the PCA pattern matches real fraud behavior.

Bulk predictions using real fraud rows will correctly identify fraud.

📌 4. Model Training Summary

The XGBoost classifier uses:

scale_pos_weight = negatives / positives

No scaling (PCA is already normalized)

Optimal fraud threshold:

fraud = probability >= 0.20


Training script:

python src/train.py --data data/creditcard.csv --out_model model/model.pkl

📌 5. API Endpoints
POST /predict — Single Transaction

Request:

{
  "features": {
    "Time": 406,
    "V1": -1.25,
    "V2": 0.62,
    "V3": -2.11,
    "...": 0,
    "V28": 0.14,
    "Amount": 150.20
  }
}


Response:

{
  "prediction": 0,
  "probability": 0.0492,
  "top_features": [
    {"feature": "Time", "value": 406},
    {"feature": "Amount", "value": 150.20},
    {"feature": "V11", "value": -3.23}
  ]
}

POST /bulk_predict — CSV Upload

Upload a CSV containing:

Time, V1, V2, ..., V28, Amount


Returns:

Fraud predictions per row

Probability scores

Downloadable CSV

UI analytics auto-update

📌 6. Project Structure
credit-card-fraud-detection/
│
├── app/
│   └── main.py                 # FastAPI backend
│
├── src/
│   ├── train.py                # Training pipeline
│   ├── predict.py              # Prediction logic
│   └── preprocess.py
│
├── frontend/
│   └── index.html              # UI
│
├── model/
│   └── model.pkl               # Pretrained XGBoost model
│
├── data/
│   └── (empty — dataset not included)
│
├── requirements.txt
├── Dockerfile
├── notebook/
│   └── notebook.ipynb
└── README.md

📌 7. Run Locally
1️⃣ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4️⃣ Open browser
http://localhost:8000

📌 8. Docker Deployment
Build the image
docker build -t fraud-detector .

Run the container
docker run -p 8000:8000 fraud-detector

Open the UI
http://localhost:8000

📌 9. Render Deployment (Production)
Steps:
✔ 1. Push your project to GitHub

Dataset must NOT be included.

✔ 2. Create a new Render Web Service

Environment: Docker

Build command: Auto

Start command: Auto

Port: 8000 (Render auto-detects)

Root directory: /

✔ 3. Deploy

Render will give a URL like:

https://your-fraud-app.onrender.com/


Frontend uses relative paths → works automatically without modification.

📌 10. Limitations (Required Section)

PCA components cannot be manually generated

Fraud predictions only spike on real PCA fraud vectors

Synthetic/random/manual inputs generally return NOT FRAUD

Dataset imbalance (0.17%) limits synthetic detectability

This behavior is realistic and matches industry-grade fraud engines.

📌 11. Conclusion

This system provides:

🎯 Accurate fraud detection

⚡ Real-time API

🖥 Modern analytics dashboard

📁 Single + bulk predictions

🐳 Docker deployment

🌐 Render-ready hosting

A complete, production-style fraud detection pipeline.