import os

import pandas as pd
from fastapi import APIRouter, HTTPException
from sklearn.model_selection import train_test_split

from ..ml.model import evaluate_model
from ..ml.preprocessing import preprocess_data
from ..ml.pytorch_model import save_pytorch_model, train_pytorch_classifier

router = APIRouter(prefix="/train", tags=["train"])


@router.post("/")
def train_model_endpoint(
    dataset_path: str, label_column: str, model_name: str, test_size: float = 0.2
):
    """
    Train a model with a given dataset.
    - dataset_path: path to the dataset file
    - label_column: target column in the CSV
    - model_name: what the saved model will be called
    - test_size: proportion of the dataset to include in the test split
    """
    df = pd.read_csv(dataset_path)

    # Preprocess data
    df = preprocess_data(df)

    # Split data into training and testing sets
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

    # Train the model
    model = train_pytorch_classifier(train_df, label_column=label_column, epochs=5)

    # Save the model
    save_path = save_pytorch_model(model, model_name)

    # Evaluate the model
    metrics = evaluate_model(model, test_df, label_column=label_column)

    return {
        "message": "Model trained successfully",
        "model_path": save_path,
        "metrics": metrics,
    }
