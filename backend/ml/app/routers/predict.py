import os

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from app.schemas_ml import PredictionRequest, PredictionResponse
from fastapi import APIRouter, HTTPException
from tensorflow import keras

router = APIRouter(tags=["predict"])


@router.post("/predict/", response_model=PredictionResponse)
def predict_ml(req: PredictionRequest):
    """
    Example: load model from saved_models, do predictions.
    """
    # 1) Find the model file
    model_base = os.path.join("saved_models", req.model_name)
    possible_paths = [model_base, f"{model_base}.joblib", f"{model_base}.h5"]
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
    if not found_path:
        raise HTTPException(404, f"Model file not found: {model_base}")

    # 2) Convert data to DF
    df = pd.DataFrame([row.dict() for row in req.data])

    # 3) If .joblib => scikit or KMeans or RF...
    if found_path.endswith(".joblib"):
        model = joblib.load(found_path)
        # Example: handle classification (predict_proba) or KMeans
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(df)
            # If binary classification => second col
            if probs.shape[1] == 1:
                probabilities = probs.flatten().tolist()
            else:
                probabilities = probs[:, 1].tolist()
            preds = model.predict(df).tolist()
        else:
            preds = model.predict(df).tolist()
            probabilities = [0.0] * len(preds)
        return {"predictions": preds, "probabilities": probabilities}

    # 4) If .h5 => TF model
    elif found_path.endswith(".h5"):
        tf_model = keras.models.load_model(found_path)
        raw_preds = tf_model.predict(df.values).flatten()
        preds = (raw_preds >= 0.5).astype(int).tolist()
        probabilities = raw_preds.tolist()
        return {"predictions": preds, "probabilities": probabilities}

    else:
        raise HTTPException(400, f"Unknown extension in {found_path}")
