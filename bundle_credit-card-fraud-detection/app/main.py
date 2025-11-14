# app/main.py

import os
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
import uvicorn
import pandas as pd
from io import StringIO

from src.predict import load_model_and_scaler, predict_transaction

# --------------------------
# CONFIG
# --------------------------
REQUIRED_COLUMNS = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model/model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model/scaler.pkl")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

LAST_CSV = None

# --------------------------
# FASTAPI APP
# --------------------------
app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Stable production-safe XGBoost predictor",
    version="1.0.0"
)

# STATIC FRONTEND
app.mount("/app", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Prevent favicon error
@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join(FRONTEND_DIR, "favicon.png")) if \
        os.path.exists(os.path.join(FRONTEND_DIR, "favicon.png")) else ""

# --------------------------
# REQUEST PAYLOAD
# --------------------------
class Transaction(BaseModel):
    features: Dict[str, float]


# --------------------------
# LOAD MODEL ON STARTUP
# --------------------------
@app.on_event("startup")
def startup_event():
    global model, scaler
    try:
        model, scaler = load_model_and_scaler(MODEL_PATH, SCALER_PATH)
        print("Model and scaler loaded successfully.")
    except Exception as e:
        print("Error loading model/scaler:", e)
        raise


# --------------------------
# PREDICT (SAFE & STABLE)
# --------------------------
@app.post("/predict")
def predict(payload: Transaction):
    try:
        features = payload.features

        # enforce stable column order
        ordered_input = {}
        for col in REQUIRED_COLUMNS:
            ordered_input[col] = float(features.get(col, 0))

        print("BACKEND RECEIVED:", ordered_input)
        result = predict_transaction(model, scaler, ordered_input)

        # compute top 3 features by absolute influence
        items = [{"feature": k, "value": float(v)} for k, v in ordered_input.items()]
        items_sorted = sorted(items, key=lambda x: abs(x["value"]), reverse=True)
        result["top_features"] = items_sorted[:3]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# --------------------------
# BULK CSV PREDICT
# --------------------------
@app.post("/bulk_predict")
async def bulk_predict(file: UploadFile = File(...)):
    global LAST_CSV

    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Upload a valid CSV file.")

        df = pd.read_csv(file.file)

        # Ensure required columns exist; fill missing with 0
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = 0

        df = df[REQUIRED_COLUMNS]

        # ----- RAW INPUT (NO SCALER) -----
        X = df.values  

        # Prediction
        probs = model.predict_proba(X)[:, 1]
        preds = (probs >= 0.20).astype(int)

        df["prediction"] = preds
        df["probability"] = probs

        # Save last CSV buffer
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        LAST_CSV = buffer

        return {
            "results": df[["prediction", "probability"]].to_dict(orient="records"),
            "csv_download": "/download_last_csv"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk processing error: {str(e)}")

# --------------------------
# DOWNLOAD LAST CSV
# --------------------------
@app.get("/download_last_csv")
def download_last_csv():
    if LAST_CSV is None:
        raise HTTPException(status_code=400, detail="No CSV generated yet.")

    return StreamingResponse(
        LAST_CSV,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fraud_results.csv"}
    )


# --------------------------
# RUN
# --------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9696, reload=True)
