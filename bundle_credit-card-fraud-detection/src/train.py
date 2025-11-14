# src/train.py

import argparse
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score


def train_model(data_path, out_model):

    print("Loading data...")
    df = pd.read_csv(data_path)

    print("Preprocessing...")
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Fraud ratio
    fraud_ratio = y.mean()
    scale_pos_weight = (len(y) - sum(y)) / sum(y)
    print(f"Detected FRAUD ratio = {fraud_ratio:.6f}")
    print(f"Using scale_pos_weight = {scale_pos_weight:.2f}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training XGBoost (optimized for fraud)...")

    model = XGBClassifier(
        n_estimators=800,
        max_depth=10,
        learning_rate=0.03,
        subsample=0.9,
        colsample_bytree=0.9,
        gamma=0,
        reg_lambda=1,
        min_child_weight=1,
        scale_pos_weight=scale_pos_weight,   # critical for fraud
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist"
    )

    model.fit(X_train, y_train)

    print("\nEvaluating model...")

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    print("\nClassification report:")
    print(classification_report(y_test, preds))

    auc = roc_auc_score(y_test, probs)
    print("ROC-AUC:", auc)

    print("\nSaving model...")
    joblib.dump(model, out_model)

    print(f"Model saved → {out_model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out_model", type=str, required=True)
    args = parser.parse_args()

    train_model(args.data, args.out_model)
