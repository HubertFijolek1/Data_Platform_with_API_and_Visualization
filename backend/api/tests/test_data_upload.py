from io import StringIO

from fastapi.testclient import TestClient


def test_upload_dataset_valid(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": "Test Dataset"}
    file_content = "name,email,address,created_at\nJohn Doe,john@example.com,123 St,2025-01-01T12:00:00"
    files = {"file": ("test_dataset.csv", StringIO(file_content), "text/csv")}
    response = client.post("/data/upload", data=data, files=files, headers=headers)
    assert response.status_code == 200, response.text
    dataset = response.json()
    assert dataset["name"] == "Test Dataset"
    assert dataset["file_name"] == "test_dataset.csv"


def test_upload_dataset_invalid_file_type(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": "Invalid File Dataset"}
    file_content = "<html></html>"
    files = {"file": ("invalid_file.html", StringIO(file_content), "text/html")}
    response = client.post("/data/upload", data=data, files=files, headers=headers)
    assert response.status_code == 400
    assert "Invalid file type" in response.text


def test_upload_dataset_unauthorized(client: TestClient):
    data = {"name": "Unauthorized Dataset"}
    file_content = "name,email\nJane Doe,jane@example.com"
    files = {"file": ("unauthorized_dataset.csv", StringIO(file_content), "text/csv")}
    response = client.post("/data/upload", data=data, files=files)
    assert response.status_code == 401
