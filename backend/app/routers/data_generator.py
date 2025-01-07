import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from faker import Faker

from .. import schemas, models, crud
from ..database import SessionLocal
from ..utils.role_checker import RoleChecker
from ..config.settings import settings

router = APIRouter(
    prefix="/data-generator",
    tags=["data-generator"],
)

fake = Faker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=schemas.DatasetRead, dependencies=[Depends(RoleChecker(["admin", "user"]))])
def generate_dataset(n_rows: int = 1000, db: Session = Depends(get_db)):
    """
    Generate a synthetic dataset with fake user data.
    """
    data = {
        "name": [fake.name() for _ in range(n_rows)],
        "email": [fake.email() for _ in range(n_rows)],
        "address": [fake.address().replace('\n', ', ') for _ in range(n_rows)],
        "created_at": [fake.date_time_this_year().isoformat() for _ in range(n_rows)]
    }
    df = pd.DataFrame(data)

    unique_id = str(uuid.uuid4())
    file_name = f"generated_{unique_id}.csv"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file_name)
    df.to_csv(file_path, index=False)

    dataset = models.Dataset(
        name=f"Generated Dataset {unique_id}",
        file_name=file_name
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset