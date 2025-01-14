import os
import shutil
import uuid
from datetime import datetime
from typing import Optional

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
    file: UploadFile, dataset_name: Optional[str] = None, overwrite: bool = False
) -> str:
    """
    Save an uploaded file and return its stored file name.
    If a file with the same name already exists and `overwrite` is False,
    raise HTTPException(400).
    """
    original_filename = sanitize_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1]

    # Decide the final file name
    if dataset_name:
        base_name = sanitize_filename(dataset_name)
        file_name = f"{base_name}{file_extension}"
    else:
        # If no name is provided, use the original file name
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A dataset with this file name already exists. "
                "Use `overwrite=true` if you want to replace it.",
            )

    # Save the new or overwritten file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_name


@router.post(
    "/upload",
    response_model=schemas.DatasetRead,
    summary="Upload a dataset file",
    description="Upload a CSV file and store metadata in the database.",
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def upload_dataset(
    name: Optional[str] = Form(None),
    file: UploadFile = File(...),
    overwrite: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Handle the upload of a CSV file. If 'name' is not provided,
    the original file's name (without extension) is used as the dataset name.
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded.",
        )

    # Restrict to CSV uploads
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV files are allowed.",
        )

    # If no dataset name is provided, use the original file name (stripped extension)
    if not name:
        name = os.path.splitext(file.filename)[0]

    # Attempt to save the file
    try:
        file_name = save_file(file, dataset_name=name, overwrite=overwrite)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )

    # Check if a dataset with the same file_name already exists in the DB
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
            # Should not happen if we already raised HTTP 400 in `save_file`,
            # but just to be safe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A dataset with this file name already exists. "
                "Use `overwrite=true` if you want to replace it.",
            )
    else:
        # Create a new dataset entry in the database
        dataset = models.Dataset(
            name=name,
            file_name=file_name,
            uploaded_at=datetime.utcnow(),
            user_id=current_user.id,
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

    return dataset
