from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base, get_db
from ..main import app

# PostgreSQL test database URL
DATABASE_URL = "postgresql://postgres:password@db:5432/data_db"

engine = create_engine(DATABASE_URL)
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
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

    # Próba rejestracji z tym samym email
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword2",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    # Próba rejestracji z tym samym username
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpassword2",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_login_user():
    # zarejestruj użytkownika
    response = client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword",
        },
    )
    assert response.status_code == 200

    # Poprawne logowanie
    response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Logowanie z błędnym hasłem
    response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Logowanie z nieistniejącym użytkownikiem
    response = client.post(
        "/auth/login",
        json={
            "username": "nonuser",
            "email": "non@example.com",
            "password": "nopassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
