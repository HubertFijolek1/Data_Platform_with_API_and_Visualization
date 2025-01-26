import pandas as pd
import torch
from app.app.ml.model import evaluate_model
from app.app.ml.pytorch_model import train_pytorch_classifier


def test_pytorch_training():
    """
    Test training of the PyTorch classifier with correct input dimensions.
    """
    # Create a sample DataFrame
    df = pd.DataFrame(
        {
            "feature1": [0.1, 0.2, 0.9, 1.0],
            "feature2": [1.2, 0.3, 0.5, 0.4],
            "label": [0, 0, 1, 1],
        }
    )

    # Train the PyTorch classifier
    model = train_pytorch_classifier(df, label_column="label", epochs=1)

    # Preprocess the DataFrame to include 'feat_sum'
    df = df.copy()
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
    if len(numeric_cols) >= 2:
        df["feat_sum"] = df[numeric_cols[0]] + df[numeric_cols[1]]

    # Create the input tensor with all required features
    X_torch = torch.tensor(df.drop(columns=["label"]).values, dtype=torch.float32)

    # Perform prediction
    with torch.no_grad():
        preds = model(X_torch)

    # Assert that the number of predictions matches the number of rows
    assert preds.shape[0] == len(df)


def test_pytorch_evaluate():
    """
    Test evaluation metrics of the PyTorch classifier.
    """
    df = pd.DataFrame(
        {
            "feature1": [0.1, 0.2, 0.9, 1.0],
            "feature2": [1.2, 0.3, 0.5, 0.4],
            "label": [0, 0, 1, 1],
        }
    )
    # Train the model
    model = train_pytorch_classifier(df, label_column="label", epochs=1)

    # Preprocess the DataFrame to include 'feat_sum'
    df = df.copy()
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
    if len(numeric_cols) >= 2:
        df["feat_sum"] = df[numeric_cols[0]] + df[numeric_cols[1]]

    # Evaluate the model
    metrics = evaluate_model(model, df, label_column="label")
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0
