import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    precision_score,
    recall_score,
)

from .preprocessing import preprocess_data


def evaluate_regression_model(model, df: pd.DataFrame, label_column: str):
    """
    Ocena modelu Keras dla regresji przy użyciu MSE.
    """
    df = preprocess_data(df)
    y_true = df[label_column].values
    X = df.drop(columns=[label_column]).values
    y_pred = model.predict(X).flatten()
    mse = mean_squared_error(y_true, y_pred)
    return {"mse": mse}


def evaluate_model(model, df: pd.DataFrame, label_column: str):
    """
    Ocena modelu Keras na zbiorze danych.
    Zwraca słownik z metrykami: accuracy, precision, recall.
    """
    df = preprocess_data(df)
    y_true = df[label_column].values
    X = df.drop(columns=[label_column]).values

    raw_preds = model.predict(X).flatten()
    # Próg 0.5 – klasyfikacja binarna
    y_pred = (raw_preds >= 0.5).astype(int).tolist()
    y_true = y_true.tolist()

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)

    return {"accuracy": acc, "precision": prec, "recall": rec}
