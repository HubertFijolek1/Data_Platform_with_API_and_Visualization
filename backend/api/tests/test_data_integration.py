import os

import pytest
from fastapi.testclient import TestClient


def test_upload_dataset_success(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    fake_file_data = "col1,col2\nval1,val2\n"
    response = client.post(
        "/data/upload",
        data={"name": "My CSV"},
        files={"file": ("test.csv", fake_file_data, "text/csv")},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    json_data = response.json()
    assert json_data["name"] == "My CSV"
    assert json_data["file_name"].endswith(".csv")

    # Check that the file was saved
    file_path = os.path.join("uploads", json_data["file_name"])
    assert os.path.exists(file_path)


def test_list_datasets_pagination(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Upload multiple datasets
    for i in range(12):
        data = f"data{i},data{i}"
        client.post(
            "/data/upload",
            data={"name": f"Dataset{i}"},
            files={"file": (f"test{i}.csv", data, "text/csv")},
            headers=headers,
        )

    # Page 1
    resp1 = client.get("/data/?page=1&page_size=5", headers=headers)
    assert resp1.status_code == 200
    items_p1 = resp1.json()
    assert len(items_p1) == 5

    # Page 2
    resp2 = client.get("/data/?page=2&page_size=5", headers=headers)
    items_p2 = resp2.json()
    assert len(items_p2) == 5


def test_delete_dataset(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Upload dataset
    response = client.post(
        "/data/upload",
        data={"name": "ToDelete"},
        files={"file": ("test_to_delete.csv", "col1,col2\n", "text/csv")},
        headers=headers,
    )
    ds = response.json()
    dataset_id = ds["id"]
    file_name = ds["file_name"]

    # Delete dataset
    del_resp = client.delete(f"/data/{dataset_id}", headers=headers)
    assert del_resp.status_code == 204

    # Check if file is removed
    file_path = os.path.join("uploads", file_name)
    assert not os.path.exists(file_path)
