import os
import uuid
from typing import List

import pandas as pd
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
from ..routers.auth import get_current_user
from ..utils.role_checker import RoleChecker

# Constants
UPLOADS_DIR = "./uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

router = APIRouter(prefix="/data", tags=["data"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility functions
def save_file(file: UploadFile, unique_id: str) -> str:
    """Save an uploaded file and return its stored path."""
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{unique_id}{file_extension}"
    file_location = os.path.join(UPLOADS_DIR, file_name)
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save file.",
        )
    return file_name


def delete_file(file_name: str):
    """Delete a file from disk."""
    file_path = os.path.join(UPLOADS_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def get_dataset_or_404(dataset_id: int, db: Session) -> models.Dataset:
    """Fetch a dataset by ID or raise an HTTP 404 error."""
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with id {dataset_id} not found.",
        )
    return dataset


def train_model(df, label_column, epochs=5):
    return 1


def save_model(model, model_name):
    return 1


def train_dataset_model(file_location: str, label_column: str, name: str):
    """Train a model using the dataset."""
    try:
        file_df = pd.read_csv(file_location)
        model = train_model(file_df, label_column=label_column, epochs=5)
        model_name = f"{name}_model"
        save_model(model, model_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during model training")


# Refactored Routes
@router.post(
    "/upload",
    response_model=schemas.DatasetRead,
    summary="Upload a dataset file",
    description="Upload a CSV or TXT file and store metadata in the database.",
)
def upload_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    train: bool = Form(False),
    label_column: str = Form(None),
):
    if not file.filename.lower().endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or TXT files are allowed.",
        )

    # Save file and create metadata
    unique_id = str(uuid.uuid4())
    file_name = save_file(file, unique_id)
    dataset = models.Dataset(name=name, file_name=file_name)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Train model if train=True
    if train:
        if not label_column:
            raise HTTPException(
                status_code=400, detail="label_column is required when train=True."
            )
        train_dataset_model(os.path.join(UPLOADS_DIR, file_name), label_column, name)
    return dataset


@router.get(
    "/",
    response_model=List[schemas.DatasetRead],
    summary="List all datasets (paginated)",
    description="Retrieve a paginated list of datasets.",
)
def get_all_datasets(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    return db.query(models.Dataset).offset(skip).limit(page_size).all()


@router.get(
    "/{dataset_id}",
    response_model=schemas.DatasetRead,
    summary="Get dataset by ID",
    description="Retrieve a specific dataset by its ID.",
)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    dataset = get_dataset_or_404(dataset_id, db)
    file_path = os.path.join(UPLOADS_DIR, dataset.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found on server: {dataset.file_name}",
        )
    return dataset


@router.delete(
    "/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a dataset by ID",
    description="Delete a specific dataset by its ID (admin only).",
)
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    admin_only: bool = Depends(RoleChecker(["admin"])),
):
    dataset = get_dataset_or_404(dataset_id, db)
    try:
        delete_file(dataset.file_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete the file.",
        )
    db.delete(dataset)
    db.commit()
