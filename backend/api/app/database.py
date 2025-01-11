import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use the environment variable for the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# print(f"DATABASE_URL is set as: {DATABASE_URL}")
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session to path operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
