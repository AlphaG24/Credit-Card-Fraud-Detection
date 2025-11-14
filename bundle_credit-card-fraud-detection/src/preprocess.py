# src/preprocess.py
"""
Preprocessing utilities for Credit Card Fraud Detection
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

FEATURE_COLUMNS = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def split_X_y(df: pd.DataFrame, test_size=0.2, random_state=42):
    X = df.drop('Class', axis=1)
    y = df['Class']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


def fit_scaler(X_train: pd.DataFrame):
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler


def transform_with_scaler(scaler: StandardScaler, X: pd.DataFrame):
    return scaler.transform(X)


def resample_smote(X, y, random_state=42):
    sm = SMOTE(random_state=random_state)
    X_res, y_res = sm.fit_resample(X, y)
    return X_res, y_res
