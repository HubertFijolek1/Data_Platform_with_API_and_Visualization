import os

from fastapi.testclient import TestClient


def test_get_dataset_by_id(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Upload a dataset
    fake_file_data = "col1,col2\nval1,val2\n"
    files = {"file": ("test_data.csv", fake_file_data, "text/csv")}
    resp = client.post(
        "/data/upload", data={"name": "MyData"}, files=files, headers=headers
    )
    assert resp.status_code == 200, resp.text
    ds = resp.json()

    # Retrieve by ID
    ds_id = ds["id"]
    r2 = client.get(f"/data/{ds_id}", headers=headers)
    assert r2.status_code == 200
    found = r2.json()
    assert found["id"] == ds_id
    assert found["name"] == "MyData"


def test_get_dataset_not_found(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.get("/data/99999", headers=headers)  # unlikely to exist
    assert r.status_code == 404
    assert "not found" in r.text
