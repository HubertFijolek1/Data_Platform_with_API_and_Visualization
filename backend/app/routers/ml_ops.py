import os
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import SessionLocal
from ..models import Dataset
from ..routers.auth import get_current_user
from ..ml.model import train_model, save_model

router = APIRouter(
    prefix="/ml",
    tags=["ml_ops"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/retrain")
def retrain_model(
    dataset_id: int,
    label_column: str,
    model_name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Retrain a model with a given dataset (by dataset_id).
    - label_column indicates the target column in the CSV
    - model_name is what the saved model will be called
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset with id {dataset_id} not found."
        )

    file_path = os.path.join("uploads", dataset.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File for dataset_id {dataset_id} not found on disk."
        )

    # Load data
    df = pd.read_csv(file_path)
    if label_column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"label_column '{label_column}' not found in dataset."
        )

    model = train_model(df, label_column=label_column, epochs=5)
    path = save_model(model, model_name)
    return {"message": "Model retrained successfully", "model_saved_path": path}
