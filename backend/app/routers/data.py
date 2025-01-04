import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import SessionLocal
from ..routers.auth import get_current_user

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

@router.post("/upload", response_model=schemas.DatasetRead)
def upload_dataset(
    name: str = Form(...),  # Part of normal form data
    file: UploadFile = File(...),  # The actual data file
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # Requires login
):
    """
    Endpoint to upload a dataset file and store relevant metadata in the DB.
    """

    # Validate file extension (basic example)
    if not file.filename.lower().endswith(('.csv', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or TXT files are allowed."
        )

    # Generate a unique file name to store it on disk (optional strategy)
    unique_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{unique_id}{file_extension}"

    # Save file to a local 'uploads' directory (you can choose a different path)
    os.makedirs("uploads", exist_ok=True)
    file_location = os.path.join("uploads", file_name)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Create a new Dataset record in the DB
    dataset = models.Dataset(
        name=name,
        file_name=file_name
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset  # FastAPI will convert this to DatasetRead

@router.get("/", response_model=List[schemas.DatasetRead])
def get_all_datasets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Retrieve a list of all uploaded datasets.
    """
    datasets = db.query(models.Dataset).all()
    return datasets

@router.get("/{dataset_id}", response_model=schemas.DatasetRead)
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
            detail=f"Dataset with id {dataset_id} not found."
        )
    return dataset