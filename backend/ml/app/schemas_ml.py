from typing import List

from pydantic import BaseModel


class RowData(BaseModel):
    feature1: float
    feature2: float


class PredictionRequest(BaseModel):
    model_name: str
    data: List[RowData]


class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]
