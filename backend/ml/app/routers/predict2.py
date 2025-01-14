import os

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

# Import from local schemas (this is the crucial fix):
from app.schemas_ml import PredictionRequest, PredictionResponse, RowData
from fastapi import APIRouter, HTTPException
from tensorflow import keras

router = APIRouter(prefix="/", tags=["predict2"])


@router.post("/predict2", response_model=PredictionResponse)
def predict2(req: PredictionRequest):
    """
    Predict with a model stored in saved_models.
    Model can be scikit-learn (joblib) or TF (h5).
    """
    # 1) Build final path
    model_path = os.path.join("saved_models", req.model_name)
    if not os.path.exists(model_path):
        possible_joblib = model_path + ".joblib"
        possible_h5 = model_path + ".h5"
        if os.path.exists(possible_joblib):
            model_path = possible_joblib
        elif os.path.exists(possible_h5):
            model_path = possible_h5
        else:
            raise HTTPException(404, f"Model file not found: {model_path}")

    # 2) Prepare input
    df = pd.DataFrame([row.dict() for row in req.data])

    if model_path.endswith(".joblib"):
        model = joblib.load(model_path)
        # scikit-learn classification or KMeans
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(df)
            if probs.shape[1] == 1:
                probabilities = probs.flatten().tolist()
            else:
                probabilities = probs[:, 1].tolist()
            preds = model.predict(df).tolist()
        else:
            preds = model.predict(df).tolist()
            probabilities = [0.0] * len(preds)
        return PredictionResponse(predictions=preds, probabilities=probabilities)

    elif model_path.endswith(".h5"):
        tf_model = keras.models.load_model(model_path)
        raw_preds = tf_model.predict(df.values).flatten()
        # threshold=0.5 => label 1 or 0
        preds = (raw_preds >= 0.5).astype(int).tolist()
        prob_list = raw_preds.tolist()
        return PredictionResponse(predictions=preds, probabilities=prob_list)
    else:
        raise HTTPException(400, f"Unknown model file extension in {model_path}")
