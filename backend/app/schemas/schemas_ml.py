from pydantic import BaseModel
from typing import List, Optional

class RowData(BaseModel):
    """
    Example schema for a single row in a classification dataset.
    Adjust the fields according to your real dataset structure.
    """
    feature1: float
    feature2: float
    # e.g. categorical features stored as strings if model expects them encoded

class PredictionRequest(BaseModel):
    model_name: str
    data: List[RowData]

class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]