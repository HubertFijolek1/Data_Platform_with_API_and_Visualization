import os

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

MODEL_DIR = os.getenv("MODEL_DIR", "saved_models/auto_trained_model/v1")
MODEL_FILE = os.path.join(MODEL_DIR, "model_pt.pt")

app = FastAPI()

# Add new routers
from app.routers import predict2, train2

app.include_router(train2.router)
app.include_router(predict2.router)


class InputData(BaseModel):
    feature1: float
    feature2: float

    @field_validator("*", mode="before")
    def convert_to_float(cls, value):
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                raise ValueError("Could not convert string to float")
        return value
