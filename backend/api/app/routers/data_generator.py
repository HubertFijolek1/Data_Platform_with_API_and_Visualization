import logging
import os

import pandas as pd
from faker import Faker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
from ..utils.role_checker import RoleChecker

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

    # Create synthetic data using Faker
    data = {
        "name": [fake.name() for _ in range(n_rows)],
        "email": [fake.email() for _ in range(n_rows)],
        "address": [fake.address().replace("\n", ", ") for _ in range(n_rows)],
        "created_at": [fake.date_time_this_year().isoformat() for _ in range(n_rows)],
    }
    df = pd.DataFrame(data)

    # Create a dataset entry with a default name to get its ID
    dataset = models.Dataset(
        name="Generated Dataset",  # Default value for name
        file_name="k",  # Placeholder file name initially
        uploaded_at=pd.Timestamp.utcnow(),  # Current timestamp
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Use dataset ID to create a unique filename
    file_name = f"generated_{dataset.id}.csv"
    uploads_dir = os.path.join(
        os.getcwd(), "uploads"
    )  # Ensure uploads directory exists
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file_name)
    df.to_csv(file_path, index=False)

    # Update the dataset with the actual file name
    dataset.file_name = file_name
    db.commit()
    db.refresh(dataset)

    logger.info(f"Synthetic dataset generated and saved as {file_name}.")
    return dataset
