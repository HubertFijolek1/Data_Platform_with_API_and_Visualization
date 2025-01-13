import os
import shutil
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..routers.auth import get_current_user
from ..utils.role_checker import RoleChecker

router = APIRouter(
    prefix="/data",
    tags=["data"],
)

UPLOADS_DIR = "./uploads"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename to prevent directory traversal and other security issues.
    """
    return os.path.basename(filename).replace(" ", "_")


def save_file(
    file: UploadFile, dataset_name: str = None, overwrite: bool = False
) -> str:
    """Save an uploaded file and return its stored file name."""
    original_filename = sanitize_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1]

    if dataset_name:
        # Use the dataset name as the file name
        base_name = sanitize_filename(dataset_name)
        file_name = f"{base_name}{file_extension}"
    else:
        # Use the original file name
        file_name = original_filename

    file_path = os.path.join(UPLOADS_DIR, file_name)

    if os.path.exists(file_path):
        if overwrite:
            # Overwrite the existing file
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to overwrite existing file: {str(e)}",
                )
        else:
            # Append a unique suffix to avoid duplicates
            unique_suffix = uuid.uuid4().hex[:8]
            file_name = (
                f"{os.path.splitext(file_name)[0]}_{unique_suffix}{file_extension}"
            )
            file_path = os.path.join(UPLOADS_DIR, file_name)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_name


@router.post(
    "/upload",
    response_model=schemas.DatasetRead,
    summary="Upload a dataset file",
    description="Upload a CSV or TXT file and store metadata in the database.",
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def upload_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    overwrite: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded.",
        )

    if file.content_type not in ["text/csv", "application/vnd.ms-excel", "text/plain"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV or TXT files are allowed.",
        )

    # If no dataset name is provided, use the original file name without extension
    if not name:
        name = os.path.splitext(file.filename)[0]

    # Save the file
    try:
        file_name = save_file(file, dataset_name=name, overwrite=overwrite)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )

    # Check if a dataset with the same file_name exists
    existing_dataset = (
        db.query(models.Dataset).filter(models.Dataset.file_name == file_name).first()
    )

    if existing_dataset:
        if overwrite:
            # Update the existing dataset's metadata
            existing_dataset.name = name
            existing_dataset.uploaded_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_dataset)
            dataset = existing_dataset
        else:
            # This should not happen due to unique constraint and overwrite handling
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dataset with this file name already exists.",
            )
    else:
        # Create a new dataset entry in the database
        dataset = models.Dataset(
            name=name,
            file_name=file_name,
            uploaded_at=datetime.utcnow(),
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

    return dataset
