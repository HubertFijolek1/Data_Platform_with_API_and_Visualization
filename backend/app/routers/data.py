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
from ..ml.model import save_model, train_model
from ..routers.auth import get_current_user
from ..utils.role_checker import RoleChecker

router = APIRouter(
    prefix="/data",
    tags=["data"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/upload",
    response_model=schemas.DatasetRead,
    summary="Upload a dataset file",
    description="Upload a CSV or TXT file and store metadata in the database.",
)
def upload_dataset(
    name: str = Form(...),  # Part of normal form data
    file: UploadFile = File(...),  # The actual data file
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # Requires login
    train: bool = Form(False),
    label_column: str = Form(None),
):
    """
    Endpoint to upload a dataset file and store relevant metadata in the DB.
    """

    if not file.filename.lower().endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or TXT files are allowed.",
        )

    unique_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{unique_id}{file_extension}"

    os.makedirs("uploads", exist_ok=True)
    file_location = os.path.join("uploads", file_name)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    dataset = models.Dataset(name=name, file_name=file_name)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # If train is True, automatically load CSV into memory, train model, and save
    if train:
        if not label_column:
            raise HTTPException(
                status_code=400, detail="label_column is required when train=True."
            )
        file_df = pd.read_csv(file_location)  # For simplicity
        model = train_model(file_df, label_column=label_column, epochs=5)
        model_name = f"{name}_model"
        save_model(model, model_name)

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
    """
    Retrieve a paginated list of datasets.
    """
    skip = (page - 1) * page_size
    datasets = db.query(models.Dataset).offset(skip).limit(page_size).all()
    return datasets


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
    """
    Retrieve details about a specific dataset by ID.
    """
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with id {dataset_id} not found.",
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
    # Only admins can delete
    admin_only: bool = Depends(RoleChecker(["admin"])),
):
    """
    Delete a dataset by its ID. Only users with the
    'admin' role can perform this operation.
    """
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with id {dataset_id} not found.",
        )

    # IT also remove the file from disk if it exists:
    file_path = os.path.join("uploads", dataset.file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(dataset)
    db.commit()
    return  # 204 No Content means success without response body


# @router.get("/limited")
# @limiter.limit("5/minute")  # only 5 calls allowed per minute
# def limited_endpoint(request: Request):
#     return {"message": "Rate-limited endpoint"}
