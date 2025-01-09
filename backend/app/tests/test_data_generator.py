import pytest
import os
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from backend.app.database import get_db
from backend.app import crud, schemas


@pytest.fixture(scope="session")
def auth_token(client: TestClient):
    # Register a test user
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200

    # Login the test user
    response = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_generate_dataset(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/data-generator/generate", json={"n_rows": 500}, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "file_name" in data
    assert "uploaded_at" in data

    # Expected file name based on dataset ID
    expected_file_name = f"generated_{data['id']}.csv"
    assert data["file_name"] == expected_file_name

    # Check that the file exists in uploads
    file_path = os.path.join("backend", "uploads", expected_file_name)
    assert os.path.exists(file_path)


def test_generate_dataset_unauthorized(client: TestClient):
    # Attempt to generate dataset without authentication
    response = client.post("/data-generator/generate", json={"n_rows": 500})
    assert response.status_code == 401


def test_generate_dataset_invalid_role(client: TestClient):
    # Register a user with a role that is not allowed to generate data
    response = client.post(
        "/auth/register",
        json={
            "username": "regularuser",
            "email": "regularuser@example.com",
            "password": "regularpassword",
        },
    )
    assert response.status_code == 200

    # Manually change the user's role to 'guest' in the database
    db: Session = next(get_db())  # Ensure get_db is imported
    user = crud.get_user_by_email(db, email="regularuser@example.com")
    user.role = "guest"
    db.add(user)
    db.commit()

    # Login the guest user
    response = client.post(
        "/auth/login",
        json={"email": "regularuser@example.com", "password": "regularpassword"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    # Attempt to generate dataset with guest role
    response = client.post(
        "/data-generator/generate", json={"n_rows": 500}, headers=headers
    )
    assert response.status_code == 403
