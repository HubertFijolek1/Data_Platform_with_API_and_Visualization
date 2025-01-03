from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app import models

# PostgreSQL test database URL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/data_db"

engine = create_engine(
    DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

    # Próba rejestracji z tym samym email
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "test@example.com", "password": "testpassword2"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    # Próba rejestracji z tym samym username
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test2@example.com", "password": "testpassword2"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"
