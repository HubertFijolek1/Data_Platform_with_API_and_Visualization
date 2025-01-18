import os
from io import StringIO

import pytest
from fastapi.testclient import TestClient


def test_train2_logistic_regression_with_text_columns(
    client: TestClient, auth_token: str
):
    """
    1) Upload a small CSV with text columns
    2) Call /ml/train2 with algorithm='LogisticRegression'
    3) Confirm label encoding works, returns 200, saves model
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    csv_data = """Name,Feature1,Feature2,Label
John,0.5,0.6,ClassA
Alice,0.7,0.1,ClassB
Bob,0.1,0.9,ClassA
Dave,0.9,0.3,ClassB
"""
    files = {"file": ("text_columns.csv", StringIO(csv_data), "text/csv")}
    # Upload
    upload_resp = client.post(
        "/data/upload", files=files, data={"name": "TextColsDataset"}, headers=headers
    )
    assert upload_resp.status_code == 200, upload_resp.text
    uploaded_ds = upload_resp.json()
    dataset_path = os.path.join("uploads", uploaded_ds["file_name"])

    # Train
    request_payload = {
        "dataset_path": dataset_path,
        "label_column": "Label",
        "algorithm": "LogisticRegression",
        "hyperparams": {"C": 1.0},
    }
    train_resp = client.post("/ml/train2", json=request_payload, headers=headers)
    assert train_resp.status_code == 200, train_resp.text
    resp_data = train_resp.json()
    assert resp_data["status"] == "ok"
    assert os.path.exists(os.path.join("saved_models", resp_data["model_file"]))


def test_train2_kmeans_text_columns(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = """City,SomeFeature,Label
London,1.2,Cluster1
Paris,3.4,Cluster2
Berlin,2.1,Cluster2
London,1.3,Cluster1
"""
    files = {"file": ("text_kmeans.csv", StringIO(csv_data), "text/csv")}
    # Upload
    up = client.post(
        "/data/upload", files=files, data={"name": "KMeansText"}, headers=headers
    )
    assert up.status_code == 200
    ds = up.json()
    path = os.path.join("uploads", ds["file_name"])

    payload = {
        "dataset_path": path,
        "label_column": "Label",  # won't matter for KMeans
        "algorithm": "KMeans",
        "hyperparams": {"n_clusters": 2},
    }
    resp = client.post("/ml/train2", json=payload, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["status"] == "ok"
    assert os.path.exists(os.path.join("saved_models", data["model_file"]))


def test_train2_invalid_label_column(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "F1,F2,RealLabel\n0.3,0.5,A\n0.2,0.4,B"
    files = {"file": ("invalid_label.csv", StringIO(csv_data), "text/csv")}
    up = client.post(
        "/data/upload", files=files, data={"name": "MissingLabelCol"}, headers=headers
    )
    assert up.status_code == 200
    ds = up.json()
    path = os.path.join("uploads", ds["file_name"])

    payload = {
        "dataset_path": path,
        "label_column": "FakeLabel",  # not in CSV
        "algorithm": "LogisticRegression",
    }
    resp = client.post("/ml/train2", json=payload, headers=headers)
    assert resp.status_code == 400
    assert "not found in CSV" in resp.text


def test_train2_unsupported_algo(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "FeatA,Label\n1,CatA\n2,CatB"
    files = {"file": ("unknown_algo.csv", StringIO(csv_data), "text/csv")}
    up = client.post(
        "/data/upload", files=files, data={"name": "UnknownAlgo"}, headers=headers
    )
    assert up.status_code == 200
    ds = up.json()
    path = os.path.join("uploads", ds["file_name"])

    payload = {
        "dataset_path": path,
        "label_column": "Label",
        "algorithm": "SuperDuperForest",
    }
    resp = client.post("/ml/train2", json=payload, headers=headers)
    assert resp.status_code == 400
    assert "Unsupported algorithm" in resp.text


def test_train2_empty_dataset(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "feature,label\n"  # no data
    files = {"file": ("empty.csv", StringIO(csv_data), "text/csv")}
    up = client.post(
        "/data/upload", files=files, data={"name": "EmptyDS"}, headers=headers
    )
    assert up.status_code == 200
    ds = up.json()
    path = os.path.join("uploads", ds["file_name"])

    payload = {
        "dataset_path": path,
        "label_column": "label",
        "algorithm": "LogisticRegression",
    }
    resp = client.post("/ml/train2", json=payload, headers=headers)
    assert resp.status_code == 400
    assert "Dataset is empty" in resp.text
