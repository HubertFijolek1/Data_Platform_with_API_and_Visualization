import os

import pytest
from fastapi.testclient import TestClient


def test_generate_dataset(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "n_rows": 500,
        "columns": ["user_id", "name"],
        "dataset_name": "GenUsers",
        "filename": None,
        "overwrite": False,
    }
    response = client.post("/data-generator/generate", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == "GenUsers"
    # file existence
    file_path = os.path.join("uploads", data["file_name"])
    assert os.path.exists(file_path)


def test_generate_dataset_unauthorized(client: TestClient):
    payload = {
        "n_rows": 300,
        "columns": ["email", "age"],
        "dataset_name": "Unauthorized",
    }
    r = client.post("/data-generator/generate", json=payload)
    assert r.status_code == 401


def test_generate_dataset_conflict_overwrite(client: TestClient, auth_token: str):
    """
    1) Generate a dataset with name 'ConflictDS', file 'Conflict.csv'
    2) Repeat with same file -> 409 unless overwrite=True
    3) Then overwrite
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "n_rows": 100,
        "columns": ["user_id"],
        "dataset_name": "ConflictDS",
        "filename": "Conflict.csv",
        "overwrite": False,
    }
    first = client.post("/data-generator/generate", json=payload, headers=headers)
    assert first.status_code == 200
    ds1 = first.json()

    # repeat => conflict
    second = client.post("/data-generator/generate", json=payload, headers=headers)
    assert second.status_code == 409

    # now overwrite
    payload["overwrite"] = True
    third = client.post("/data-generator/generate", json=payload, headers=headers)
    assert third.status_code == 200
