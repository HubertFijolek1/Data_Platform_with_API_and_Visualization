import os

import joblib
import pandas as pd
import tensorflow as tf
from app.database import get_db
from app.models.models import Dataset
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sqlalchemy.orm import Session
from tensorflow import keras

router = APIRouter(prefix="/ml", tags=["ml_ops"])


class Train2Request(BaseModel):
    dataset_id: int
    label_column: str
    algorithm: str
    hyperparams: dict = {}


@router.post("/train2")
def train_model_any(request: Train2Request, db: Session = next(get_db())):
    """
    Train scikit-learn or TF models.
    Saves model to disk with joblib or .h5
    """
    # 1) Locate dataset
    ds = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
    if not ds:
        raise HTTPException(404, f"Dataset {request.dataset_id} not found")

    dataset_path = os.path.join("uploads", ds.file_name)
    if not os.path.exists(dataset_path):
        raise HTTPException(404, f"Dataset file not found on disk: {ds.file_name}")

    df = pd.read_csv(dataset_path)
    if df.empty:
        raise HTTPException(400, "Dataset is empty")

    algo = request.algorithm.lower()
    if algo in ["logisticregression", "randomforestclassifier"]:
        # We expect a label column
        if request.label_column not in df.columns:
            raise HTTPException(
                400, f"Label column '{request.label_column}' not in CSV"
            )
        X = df.drop(columns=[request.label_column])
        y = df[request.label_column]

        if algo == "logisticregression":
            c_val = float(request.hyperparams.get("C", 1.0))
            model = LogisticRegression(C=c_val, max_iter=1000)
        else:
            n_est = int(request.hyperparams.get("n_estimators", 100))
            model = RandomForestClassifier(n_estimators=n_est)

        model.fit(X, y)
        model_filename = f"{algo}_dataset_{ds.id}.joblib"
        joblib.dump(model, os.path.join("saved_models", model_filename))

        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained {algo} on dataset {ds.id}",
        }

    elif algo == "kmeans":
        # unsupervised
        n_clusters = int(request.hyperparams.get("n_clusters", 2))
        km = KMeans(n_clusters=n_clusters)
        km.fit(df)  # or X = ...
        model_filename = f"kmeans_dataset_{ds.id}.joblib"
        joblib.dump(km, os.path.join("saved_models", model_filename))
        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained KMeans with {n_clusters} clusters",
        }

    elif algo == "tensorflow_classifier":
        # Very simple binary classifier
        if request.label_column not in df.columns:
            raise HTTPException(
                400, f"Label column '{request.label_column}' not in CSV"
            )
        X = df.drop(columns=[request.label_column]).values
        y = df[request.label_column].values

        # Build simple TF model
        model = keras.Sequential()
        model.add(keras.layers.Dense(16, activation="relu", input_shape=(X.shape[1],)))
        model.add(keras.layers.Dense(1, activation="sigmoid"))
        model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

        epochs = int(request.hyperparams.get("epochs", 5))
        model.fit(X, y, epochs=epochs, batch_size=32, verbose=1)

        model_filename = f"tf_dataset_{ds.id}.h5"
        save_path = os.path.join("saved_models", model_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.save(save_path)

        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained TF classifier for dataset {ds.id}",
        }
    else:
        raise HTTPException(400, f"Unsupported algorithm: {request.algorithm}")
