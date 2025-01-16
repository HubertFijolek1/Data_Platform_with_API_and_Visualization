import os

import joblib
import pandas as pd
import tensorflow as tf
from app.schemas_ml import PredictionRequest, PredictionResponse
from fastapi import APIRouter, HTTPException
from tensorflow import keras

# Use prefix="/ml" to fix the AssertionError
router = APIRouter(prefix="/ml", tags=["predict2"])


@router.post("/predict2", response_model=PredictionResponse)
def predict2(req: PredictionRequest):
    """
    Predict with a model stored in saved_models.
    Model can be scikit-learn (joblib) or TF (h5).

    Final route => /ml/predict2
    """
    base_path = os.path.join("saved_models", req.model_name)
    possible_paths = [base_path, base_path + ".joblib", base_path + ".h5"]

    found_path = None
    for p in possible_paths:
        if os.path.exists(p):
            found_path = p
            break

    if not found_path:
        raise HTTPException(404, f"Model file not found for: {req.model_name}")

    df = pd.DataFrame([row.dict() for row in req.data])

    # scikit-learn / joblib
    if found_path.endswith(".joblib"):
        model = joblib.load(found_path)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(df)
            # If binary classification => second column
            if probs.shape[1] == 1:
                probabilities = probs.flatten().tolist()
            else:
                probabilities = probs[:, 1].tolist()
            preds = model.predict(df).tolist()
        else:
            # e.g., KMeans
            preds = model.predict(df).tolist()
            probabilities = [0.0] * len(preds)
        return PredictionResponse(predictions=preds, probabilities=probabilities)

    # TensorFlow (.h5)
    elif found_path.endswith(".h5"):
        tf_model = keras.models.load_model(found_path)
        raw_preds = tf_model.predict(df.values).flatten()
        preds = (raw_preds >= 0.5).astype(int).tolist()
        prob_list = raw_preds.tolist()
        return PredictionResponse(predictions=preds, probabilities=prob_list)

    else:
        raise HTTPException(400, f"Unknown model file extension in {found_path}")
