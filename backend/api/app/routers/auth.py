import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import schemas
from ..config.settings import settings
from ..crud import (
    create_user,
    get_password_hash,
    get_user_by_email,
    get_user_by_username,
)
from ..database import SessionLocal
from ..models import User
from ..services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

logger = logging.getLogger("app")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    logger.info(f"Authenticated user: {user.username}")
    return user


@router.post("/register", response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Attempting to register user: {user.username}")
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"Registration failed: Email {user.email} already registered.")
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Registration failed: Username {user.username} already taken.")
        raise HTTPException(status_code=400, detail="Username already taken")
    created_user = create_user(db=db, user=user)
    logger.info(f"User registered successfully: {created_user.username}")
    return created_user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.debug(f"Login attempt for email: {credentials.email}")
    try:
        access_token = login_user(credentials, db)
        logger.info(f"User logged in successfully: {credentials.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        logger.warning(f"Login failed for email: {credentials.email} - {e.detail}")
        raise e


@router.get("/me", response_model=schemas.UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    logger.debug(f"Fetching profile for user: {current_user.username}")
    return current_user


@router.put("/update_profile")
def update_profile(
    email: str = None,
    password: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the current user's email or password (or both).
    """
    logger.debug(f"Update profile request for user: {current_user.username}")
    updated = False
    if email:
        # Check if email is already taken
        existing_user = get_user_by_email(db, email=email)
        if existing_user and existing_user.id != current_user.id:
            logger.warning(
                f"Email update failed: {email} already registered by another user."
            )
            raise HTTPException(
                status_code=400, detail="Email already registered by another user."
            )
        current_user.email = email
        updated = True

    if password:
        # Hash and set new password
        hashed = get_password_hash(password)
        current_user.hashed_password = hashed
        updated = True

    if updated:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        logger.info(f"Profile updated successfully for user: {current_user.username}")
        return {"message": "Profile updated successfully."}
    else:
        logger.debug(f"No changes made to profile for user: {current_user.username}")
        return {"message": "No changes made."}
