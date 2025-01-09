import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/data_db")

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
