import os

import pytest
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models.models import User
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Recreate the tables for a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create a test user
    db = SessionLocal()
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="fakehashed",
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    with TestClient(app) as c:
        yield c


def test_upload_dataset_success(client):
    # Let's pretend it's not protected, or we have a token (not shown).
    fake_file_data = "col1,col2\nval1,val2\n"
    response = client.post(
        "/data/upload",
        data={"name": "My CSV"},
        files={"file": ("test.csv", fake_file_data, "text/csv")},
    )

    assert response.status_code == 200, response.text
    json_data = response.json()
    assert json_data["name"] == "My CSV"
    assert json_data["file_name"].endswith(".csv")

    # Check that the file was saved
    file_path = os.path.join("uploads", json_data["file_name"])
    assert os.path.exists(file_path)


def test_upload_dataset_wrong_format(client):
    fake_file_data = "col1,col2\nval1,val2\n"
    response = client.post(
        "/data/upload",
        data={"name": "Bad Format"},
        files={"file": ("test.pdf", fake_file_data, "application/pdf")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV or TXT files are allowed."


def test_list_datasets_pagination(client):
    # Upload multiple datasets
    for i in range(15):
        fake_file_data = f"data{i},data{i}"
        client.post(
            "/data/upload",
            data={"name": f"Dataset{i}"},
            files={"file": (f"test{i}.csv", fake_file_data, "text/csv")},
        )

    # Get page 1
    response_page1 = client.get("/data/?page=1&page_size=5")
    assert response_page1.status_code == 200
    data_page1 = response_page1.json()
    assert len(data_page1) == 5
    assert data_page1[0]["name"] == "Dataset0"

    # Get page 2
    response_page2 = client.get("/data/?page=2&page_size=5")
    assert len(response_page2.json()) == 5
    assert response_page2.json()[0]["name"] == "Dataset5"


def test_delete_dataset(client):
    # Upload dataset
    response = client.post(
        "/data/upload",
        data={"name": "ToDelete"},
        files={"file": ("test_to_delete.csv", "col1,col2\n", "text/csv")},
    )
    dataset_id = response.json()["id"]
    file_name = response.json()["file_name"]

    # Delete dataset
    delete_resp = client.delete(f"/data/{dataset_id}")
    assert delete_resp.status_code == 204

    # Check if file is removed
    file_path = os.path.join("uploads", file_name)
    assert not os.path.exists(file_path)
