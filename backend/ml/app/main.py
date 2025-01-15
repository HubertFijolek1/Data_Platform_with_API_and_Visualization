import os
from typing import List

import pandas as pd
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

# Assuming you have a saved PyTorch model
from .ml.pytorch_model import SimplePyTorchModel  # Import my PyTorch model class

# Use an environment variable to specify the model directory.
# This makes it easier to change without modifying the code.
MODEL_DIR = os.getenv("MODEL_DIR", "saved_models/auto_trained_model/v1")
MODEL_FILE = os.path.join(MODEL_DIR, "model_pt.pt")  # Assuming you saved as .pt

# Check if the model directory exists before attempting to load
if os.path.exists(MODEL_FILE):
    try:
        # Load the PyTorch model's state_dict
        model = SimplePyTorchModel(
            input_dim=2
        )  # Replace with your actual input dimension
        model.load_state_dict(torch.load(MODEL_FILE))
        model.eval()  # Set the model to evaluation mode
    except Exception as e:
        print(f"Error loading model from {MODEL_FILE}: {e}")
        model = None
else:
    print(f"Model file {MODEL_FILE} does not exist. Skipping model loading.")
    model = None

app = FastAPI()

# Add new routers
from app.routers import predict2, train, train2

app.include_router(train2.router)
app.include_router(predict2.router)
app.include_router(train.router)


# Example input data schema
class InputData(BaseModel):
    feature1: float
    feature2: float
    # ... other features

    @validator("*", pre=True)
    def convert_to_float(cls, value):
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                raise ValueError("Could not convert string to float")
        return value


@app.post("/predict/")
async def predict(data: List[InputData]):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Convert input data to DataFrame
    input_data = [item.dict() for item in data]
    df = pd.DataFrame(input_data)

    # Convert DataFrame to PyTorch tensor
    # Ensure the data type matches the model's expected input
    try:
        input_tensor = torch.tensor(df.values, dtype=torch.float32)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error converting data to tensor: {e}"
        )

    # Perform your ML prediction logic here using PyTorch
    try:
        with torch.no_grad():
            predictions = model(input_tensor)
            result = predictions.tolist()  # Example: Convert results to list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

    return {"result": result}
