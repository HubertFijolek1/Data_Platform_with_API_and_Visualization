from sqlalchemy.orm import Session
from .. import crud, schemas
from ..models import User
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from ..config.settings import settings


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return None
    if not crud.verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def login_user(credentials: schemas.UserLogin, db: Session) -> str:
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return access_token
