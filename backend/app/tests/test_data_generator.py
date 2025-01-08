# backend/tests/test_data_generator.py
import pytest
from sqlalchemy.orm import Session
from fastapi import status

from ...app import crud, schemas


@pytest.fixture
def auth_token(client: "TestClient"):
    # Register a test user
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200

    # Login the test user
    response = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_generate_dataset(client: "TestClient", auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/data-generator/generate", json={"n_rows": 500}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "file_name" in data
    assert "uploaded_at" in data


def test_generate_dataset_unauthorized(client: "TestClient"):
    # Attempt to generate dataset without authentication
    response = client.post("/data-generator/generate", json={"n_rows": 500})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_generate_dataset_invalid_role(client: "TestClient"):
    # Register a user with a role that is not allowed to generate data
    response = client.post(
        "/auth/register",
        json={"username": "regularuser", "email": "regularuser@example.com", "password": "regularpassword"}
    )
    assert response.status_code == 200

    # Manually change the user's role to 'guest' in the database
    db: Session = next(client.application.dependency_overrides[get_db]())
    user = crud.get_user_by_email(db, email="regularuser@example.com")
    user.role = "guest"
    db.add(user)
    db.commit()

    # Login the guest user
    response = client.post(
        "/auth/login",
        json={"email": "regularuser@example.com", "password": "regularpassword"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    # Attempt to generate dataset with guest role
    response = client.post("/data-generator/generate", json={"n_rows": 500}, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN