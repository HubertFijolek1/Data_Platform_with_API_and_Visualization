import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from faker import Faker
import logging
from typing import Optional

from .. import schemas, models, crud
from ..database import SessionLocal
from ..utils.role_checker import RoleChecker
from ..config.settings import settings

router = APIRouter(
    prefix="/data-generator",
    tags=["data-generator"],
)

fake = Faker()

logger = logging.getLogger("app")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/generate",
    response_model=schemas.DatasetRead,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def generate_dataset(n_rows: int = 1000, db: Session = Depends(get_db)):
    """
    Generate a synthetic dataset with fake user data.
    """
    logger.debug(f"Generating synthetic dataset with {n_rows} rows.")
    data = {
        "name": [fake.name() for _ in range(n_rows)],
        "email": [fake.email() for _ in range(n_rows)],
        "address": [fake.address().replace("\n", ", ") for _ in range(n_rows)],
        "created_at": [fake.date_time_this_year().isoformat() for _ in range(n_rows)],
    }
    df = pd.DataFrame(data)

    # Create a dataset entry first to get its ID
    dataset = models.Dataset(
        name=f"Generated Dataset",
        file_name="",  # Temporary, will update after saving
        uploaded_at=pd.Timestamp.utcnow(),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Use dataset ID to create a unique filename
    file_name = f"generated_{dataset.id}.csv"
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file_name)
    df.to_csv(file_path, index=False)

    # Update the dataset with the correct file name
    dataset.file_name = file_name
    db.commit()
    db.refresh(dataset)

    logger.info(f"Synthetic dataset generated and saved as {file_name}.")
    return dataset
