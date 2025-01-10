import os
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
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


UPLOADS_DIR = "./uploads"


@router.post(
    "/upload",
    response_model=schemas.DatasetRead,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def upload_dataset(
    name: str,
    file: UploadFile = File(...),
    train: bool = False,
    label_column: str = None,
    db: Session = Depends(get_db),
):
    """
    Upload a dataset file to the server.
    Optionally, trigger model training after upload.
    """
    if not name:
        raise HTTPException(status_code=400, detail="Dataset name is required.")

    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only CSV files are allowed."
        )

    # Save the uploaded file
    uploads_dir = os.path.join("uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    file_location = os.path.join(uploads_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create a new dataset entry in the database
    dataset = models.Dataset(
        name=name, file_name=file.filename, uploaded_at=datetime.utcnow()
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Optionally trigger model training
    if train:
        if not label_column:
            raise HTTPException(
                status_code=400, detail="Label column is required for training."
            )

        # Here I can add logic to trigger model training asynchronously in the future
        print(
            f"Triggering model training for dataset {dataset.name} "
            f"with label column {label_column}"
        )

    return dataset


def save_file(file: UploadFile, unique_id: str) -> str:
    """Save an uploaded file and return its stored path."""
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{unique_id}{file_extension}"
    file_location = os.path.join(UPLOADS_DIR, file_name)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file_name
