import os
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
from ..routers.auth import get_current_user

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

    query = db.query(models.Dataset)
    if current_user.role != "admin":
        query = query.filter(models.Dataset.user_id == current_user.id)

    return query.offset(skip).limit(page_size).all()


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
    description="Delete a specific dataset by its ID (owner or admin).",
)
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    dataset = get_dataset_or_404(dataset_id, db)

    # If not admin and not the dataset owner => 403
    if current_user.role != "admin" and dataset.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to perform this action"
        )

    try:
        delete_file(dataset.file_name)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete the file.",
        )
    db.delete(dataset)
    db.commit()
