import pandas as pd
import pytest
import torch
from app.ml.model import evaluate_model
from app.ml.pytorch_model import train_pytorch_classifier


def test_pytorch_training():
    df = pd.DataFrame(
        {
            "feature1": [0.1, 0.2, 0.9, 1.0],
            "feature2": [1.2, 0.3, 0.5, 0.4],
            "label": [0, 0, 1, 1],
        }
    )
    model = train_pytorch_classifier(df, label_column="label", epochs=1)
    X_torch = torch.tensor(df[["feature1", "feature2"]].values, dtype=torch.float32)
    with torch.no_grad():
        preds = model(X_torch)
    assert preds.shape[0] == len(df)


def test_pytorch_evaluate():
    df = pd.DataFrame(
        {
            "feature1": [0.1, 0.2, 0.9, 1.0],
            "feature2": [1.2, 0.3, 0.5, 0.4],
            "label": [0, 0, 1, 1],
        }
    )
    # same training
    model = train_pytorch_classifier(df, label_column="label", epochs=1)
    metrics = evaluate_model(model, df, label_column="label")
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0
