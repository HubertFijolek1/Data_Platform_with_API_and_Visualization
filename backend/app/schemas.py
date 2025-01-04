from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

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
        orm_mode = True
