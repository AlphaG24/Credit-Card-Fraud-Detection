# src/predict.py
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, Optional

DEFAULT_THRESHOLD = 0.20  # tuned for imbalanced dataset

def load_model_and_scaler(model_path: str, scaler_path: Optional[str] = None) -> Tuple[object, Optional[object]]:
    """
    Load model and scaler using joblib.
    Returns (model, scaler_or_none).
    """
    model = joblib.load(model_path)
    scaler = None
    if scaler_path:
        try:
            scaler = joblib.load(scaler_path)
        except Exception:
            # If scaler fails to load, return None (model will be used on raw values)
            scaler = None
    return model, scaler


def predict_transaction(model: object, scaler: Optional[object], features: dict, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """
    features: dict with keys exactly matching:
      ["Time", "V1".."V28", "Amount"]
    scaler: if provided, must accept DataFrame with same columns (scaler.feature_names_in_ typically)
    Returns {"prediction": 0/1, "probability": float}
    """
    ordered_cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

    # Build DataFrame with exact column order (fills missing with 0)
    row = {col: float(features.get(col, 0)) for col in ordered_cols}
    df = pd.DataFrame([row], columns=ordered_cols)

    # If scaler is present, try to use it with proper column names to avoid warnings
    if scaler is not None:
        try:
            # If scaler was a sklearn pipeline/transformer fitted with feature names,
            # passing a DataFrame with same column names is safe.
            X = scaler.transform(df)
        except Exception:
            # fallback: convert to numpy and attempt transform (some scalers expect arrays)
            X = scaler.transform(df.values)
    else:
        X = df.values  # raw features (less ideal)

    # Ensure shape is (1, n_features)
    X = np.asarray(X).reshape(1, -1)

    # Model should support predict_proba
    prob = float(model.predict_proba(X)[0][1])
    pred = int(prob >= threshold)

    return {"prediction": pred, "probability": prob}
