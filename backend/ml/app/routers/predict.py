# from pydantic import BaseModel
import pandas as pd
from fastapi import APIRouter, HTTPException

from backend.api.app.schemas.schemas_ml import PredictionRequest, PredictionResponse
from backend.ml.app.ml.model import load_model

# from typing import List, Union


router = APIRouter(prefix="/predict", tags=["predict"])

# class PredictionInput(BaseModel):
#    data: List[dict]  # Each dict is a row of input data
#    model_name: str


@router.post("/", response_model=PredictionResponse)
def predict(input_data: PredictionRequest):
    """
    Predict endpoint:
    - Loads a saved Keras model by model_name
    - Predicts on the given data
    - Returns probabilities (float) and predicted labels (int)
    """
    # Attempt to load model
    model = load_model(input_data.model_name)

    if not model:
        raise HTTPException(
            status_code=404, detail=f"Model '{input_data.model_name}' not found."
        )

    # Convert list-of-dicts to a DataFrame
    df = pd.DataFrame(input_data.data)
    # Convert List[RowData] to a list of dicts, then to a DataFrame
    row_dicts = [row.dict() for row in input_data.data]
    df = pd.DataFrame(row_dicts)

    # If the DataFrame is empty or has no columns, return error
    if df.empty:
        raise HTTPException(status_code=400, detail="No data provided for prediction.")

    # Model expects numeric inputs; if needed, handle them or throw error
    # For now, let's assume the data is already numeric or valid

    # Return raw probabilities
    y_pred_probs = model.predict(df.values)
    # Convert probabilities (binary classification) to label
    y_pred_labels = (y_pred_probs >= 0.5).astype(int).flatten().tolist()

    # Flatten probabilities to normal Python list of floats
    y_pred_probs_list = y_pred_probs.flatten().tolist()

    return PredictionResponse(
        predictions=y_pred_labels, probabilities=y_pred_probs_list
    )
