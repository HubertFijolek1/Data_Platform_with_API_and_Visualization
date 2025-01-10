import os

import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    precision_score,
    recall_score,
)

from .preprocessing import preprocess_data


def evaluate_regression_model(model, df: pd.DataFrame, label_column: str):
    """
    Evaluate a trained Keras regression model on MSE or other metrics.
    """
    df = preprocess_data(df)
    y_true = df[label_column].values
    X = df.drop(columns=[label_column]).values

    y_pred = model.predict(X).flatten()
    mse = mean_squared_error(y_true, y_pred)
    return {"mse": mse}


def evaluate_model(model, df: pd.DataFrame, label_column: str):
    """
    Evaluate a trained Keras model on a dataset.
    Returns a dictionary of metrics: accuracy, precision, recall
    """
    df = preprocess_data(df)
    y_true = df[label_column].values
    X = df.drop(columns=[label_column]).values

    X_torch = torch.tensor(X, dtype=torch.float32)

    with torch.no_grad():
        y_pred_probs = model(X_torch)
        # Assuming model outputs probabilities, apply threshold for binary classification
        y_pred = (y_pred_probs >= 0.5).int().flatten().tolist()

    y_true = y_true.flatten().tolist()

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)

    return {"accuracy": acc, "precision": prec, "recall": rec}
