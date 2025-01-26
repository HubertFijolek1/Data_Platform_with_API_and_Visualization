import os
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.models import Dataset
from ..routers.auth import get_current_user

router = APIRouter(prefix="/ml", tags=["ml_ops"])

metrics_store = {}  # dict with keys: (model_name, version), value: dict of metrics


def save_metrics(model_name: str, version: str, metrics: dict):
    metrics_store[(model_name, version)] = metrics


def get_metrics(model_name: str, version: str):
    return metrics_store.get((model_name, version), None)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/retrain")
async def retrain_model(
    dataset_id: int,
    label_column: str,
    model_name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Triggers the retraining of a model using the backend-ml service.
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=404, detail=f"Dataset with id {dataset_id} not found."
        )

    file_path = os.path.join("uploads", dataset.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File for dataset_id {dataset_id} not found on disk.",
        )

    train_endpoint = "http://backend-ml:8000/train/"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                train_endpoint,
                json={
                    "dataset_path": os.path.abspath(file_path),
                    "label_column": label_column,
                    "model_name": model_name,
                },
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger model training: {e}"
        )


@router.get("/performance")
def get_model_performance(model_name: str, version: str = "v1"):
    """
    Return stored model metrics for the given model_name and version.
    """
    metrics = get_metrics(model_name, version)
    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for {model_name} version {version}.",
        )
    return metrics


@router.get("/models", response_model=List[str], tags=["ml_ops"])
def list_models(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Return all .joblib and .h5 files from saved_models directory
    so the user can pick them in the UI.
    """
    saved_models_dir = "saved_models"
    if not os.path.exists(saved_models_dir):
        return []
    all_files = os.listdir(saved_models_dir)
    # you might only return .joblib / .h5
    model_files = [f for f in all_files if (f.endswith(".joblib") or f.endswith(".h5"))]
    return model_files


@router.get("/metrics/{model_name}/{version}", response_model=dict, tags=["ml_ops"])
async def get_model_metrics(
    model_name: str,
    version: str = "v1",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve performance metrics for a specified model and version from the backend-ml service.
    """
    metrics_endpoint = f"http://backend-ml:8000/metrics/{model_name}/{version}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(metrics_endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json().get("detail", "Failed to retrieve metrics"),
                )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get metrics from backend-ml: {e}"
        )
