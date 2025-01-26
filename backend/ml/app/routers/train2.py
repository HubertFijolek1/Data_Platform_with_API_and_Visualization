import os

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

router = APIRouter(prefix="/ml", tags=["ml_ops"])


class Train2Request(BaseModel):
    dataset_path: str
    label_column: str
    algorithm: str
    hyperparams: dict = {}


def encode_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all object/string columns in df to numeric via LabelEncoder.
    For large or purely free-text columns, consider a more robust approach.
    """
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        le = LabelEncoder()
        # Convert column to string just in case it has mixed types
        df[col] = le.fit_transform(df[col].astype(str))
    return df


@router.post("/train2")
def train_model_any(request: Train2Request):
    """
    Train scikit-learn or TF models.

    Expects a direct path to the CSV file (dataset_path).
    We do NOT call 'app.database' or any DB session.
    """
    # 1) Ensure the CSV file exists
    if not os.path.exists(request.dataset_path):
        raise HTTPException(404, detail=f"File not found: {request.dataset_path}")

    df = pd.read_csv(request.dataset_path)
    if df.empty:
        raise HTTPException(400, detail="Dataset is empty")

    algo = request.algorithm.lower()

    # Encode all object/string columns to numeric so scikit-learn won't crash.
    df = encode_text_columns(df)

    # ----- SUPERVISED (Classification) -----
    if algo in ["logisticregression", "randomforestclassifier"]:
        # Expect a label column
        if request.label_column not in df.columns:
            raise HTTPException(
                400, detail=f"Label column '{request.label_column}' not found in CSV"
            )

        X = df.drop(columns=[request.label_column])
        y = df[request.label_column]

        if algo == "logisticregression":
            c_val = float(request.hyperparams.get("C", 1.0))
            model = LogisticRegression(C=c_val, max_iter=1000)
        else:  # randomforestclassifier
            n_est = int(request.hyperparams.get("n_estimators", 100))
            model = RandomForestClassifier(n_estimators=n_est)

        model.fit(X, y)
        model_filename = f"{algo}_{os.path.basename(request.dataset_path)}.joblib"
        os.makedirs("saved_models", exist_ok=True)
        joblib.dump(model, os.path.join("saved_models", model_filename))

        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained {algo} on {request.dataset_path}",
        }

    # ----- UNSUPERVISED (KMeans) -----
    elif algo == "kmeans":
        n_clusters = int(request.hyperparams.get("n_clusters", 2))
        km = KMeans(n_clusters=n_clusters)
        km.fit(df)  # KMeans will also fail if it sees strings, so label-encoding helps
        model_filename = f"kmeans_{os.path.basename(request.dataset_path)}.joblib"
        os.makedirs("saved_models", exist_ok=True)
        joblib.dump(km, os.path.join("saved_models", model_filename))
        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained KMeans with {n_clusters} clusters on {request.dataset_path}",
        }

    # ----- DEEP LEARNING (TensorFlow) -----
    elif algo == "tensorflow_classifier":
        # Basic binary classifier
        if request.label_column not in df.columns:
            raise HTTPException(
                400, detail=f"Label column '{request.label_column}' not in CSV"
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

        model_filename = f"tf_{os.path.basename(request.dataset_path)}.h5"
        os.makedirs("saved_models", exist_ok=True)
        model.save(os.path.join("saved_models", model_filename))

        return {
            "status": "ok",
            "model_file": model_filename,
            "details": f"Trained TF classifier for {request.dataset_path}",
        }

    else:
        raise HTTPException(400, detail=f"Unsupported algorithm: {request.algorithm}")
