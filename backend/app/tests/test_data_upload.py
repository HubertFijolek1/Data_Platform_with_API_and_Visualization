import pytest
from fastapi import status
from io import StringIO

from ...app import crud, schemas


@pytest.fixture
def auth_token(client: "TestClient"):
    # Register a test user
    response = client.post(
        "/auth/register",
        json={
            "username": "uploader",
            "email": "uploader@example.com",
            "password": "uploadpassword",
        },
    )
    assert response.status_code == 200

    # Login the test user
    response = client.post(
        "/auth/login",
        json={"email": "uploader@example.com", "password": "uploadpassword"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_upload_dataset(client: "TestClient", auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": "Test Dataset"}
    file_content = "name,email,address,created_at\nJohn Doe,john@example.com,123 Elm Street,2025-01-01T12:00:00"
    files = {"file": ("test_dataset.csv", StringIO(file_content), "text/csv")}
    response = client.post("/data/upload", data=data, files=files, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    dataset = response.json()
    assert dataset["name"] == "Test Dataset"
    assert dataset["file_name"] == "test_dataset.csv"
    assert "uploaded_at" in dataset


def test_upload_dataset_invalid_file_type(client: "TestClient", auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": "Invalid File Dataset"}
    file_content = "<html></html>"
    files = {"file": ("invalid_file.html", StringIO(file_content), "text/html")}
    response = client.post("/data/upload", data=data, files=files, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_upload_dataset_unauthorized(client: "TestClient"):
    # Attempt to upload dataset without authentication
    data = {"name": "Unauthorized Dataset"}
    file_content = "name,email,address,created_at\nJane Doe,jane@example.com,456 Oak Avenue,2025-01-02T15:30:00"
    files = {"file": ("unauthorized_dataset.csv", StringIO(file_content), "text/csv")}
    response = client.post("/data/upload", data=data, files=files)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
