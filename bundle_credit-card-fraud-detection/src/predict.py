import joblib
import numpy as np
import pandas as pd

# ------------------------------
# LOAD ONLY MODEL (NO SCALER USED)
# ------------------------------
def load_model_and_scaler(model_path, scaler_path=None):
    model = joblib.load(model_path)
    return model, None



# ------------------------------
# PREDICT SINGLE INSTANCE (RAW INPUT)
# ------------------------------
def predict_transaction(model, scaler_unused, features: dict):

    # Correct order expected by training
    ordered_cols = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

    # Build DataFrame exactly like training input
    df = pd.DataFrame([[features.get(col, 0) for col in ordered_cols]], 
                      columns=ordered_cols)

    # Remove scaling entirely
    df_scaled = df.values   # NO SCALER
    prob = float(model.predict_proba(df_scaled)[0][1])


    # Threshold tuned: 0.20 gives balanced fraud detection
    pred = int(prob >= 0.20)

    return {
        "prediction": pred,
        "probability": prob
    }
