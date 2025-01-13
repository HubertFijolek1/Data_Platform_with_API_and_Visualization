from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class DatasetCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    file_name: str
    uploaded_at: datetime


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class DatasetCreate(BaseModel):
    name: str


class DatasetRead(BaseModel):
    id: int
    name: str
    file_name: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GenerateDatasetRequest(BaseModel):
    """
    Pydantic model for handling dataset generation requests.
    """

    n_rows: int = Field(
        ..., ge=100, le=100000, description="Number of rows (min: 100, max: 100,000)"
    )
    columns: List[str] = Field(
        ..., description="List of columns to include in the dataset"
    )
    dataset_name: str = Field(..., description="Name of the dataset")
    filename: Optional[str] = Field(
        default=None, description="Optional custom file name (e.g., 'MyData.csv')"
    )
    overwrite: bool = Field(
        default=False, description="If True and filename already exists, overwrite it"
    )
