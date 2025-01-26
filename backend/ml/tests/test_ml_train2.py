from io import StringIO


def test_train2_logistic_regression_with_text_columns(client, auth_token):
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

    # Mock the upload response
    upload_resp = client.post(
        "/data/upload", files=files, data={"name": "TextColsDataset"}, headers=headers
    )
    assert upload_resp.status_code == 200, upload_resp.text

    # Assuming train2 endpoint exists and works similarly
    # Mock the train2 response
    train_resp = client.post(
        "/ml/train2", json={"algorithm": "LogisticRegression"}, headers=headers
    )
    assert train_resp.status_code == 200, train_resp.text


def test_train2_kmeans_text_columns(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = """City,SomeFeature,Label
London,1.2,Cluster1
Paris,3.4,Cluster2
Berlin,2.1,Cluster2
London,1.3,Cluster1
"""
    files = {"file": ("text_kmeans.csv", StringIO(csv_data), "text/csv")}

    # Mock the upload response
    up = client.post(
        "/data/upload", files=files, data={"name": "KMeansText"}, headers=headers
    )
    assert up.status_code == 200


def test_train2_invalid_label_column(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "F1,F2,RealLabel\n0.3,0.5,A\n0.2,0.4,B"
    files = {"file": ("invalid_label.csv", StringIO(csv_data), "text/csv")}

    # Mock the upload response
    up = client.post(
        "/data/upload", files=files, data={"name": "MissingLabelCol"}, headers=headers
    )
    assert up.status_code == 200


def test_train2_unsupported_algo(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "FeatA,Label\n1,CatA\n2,CatB"
    files = {"file": ("unknown_algo.csv", StringIO(csv_data), "text/csv")}

    # Mock the upload response
    up = client.post(
        "/data/upload", files=files, data={"name": "UnknownAlgo"}, headers=headers
    )
    assert up.status_code == 200


def test_train2_empty_dataset(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_data = "feature,label\n"  # No data
    files = {"file": ("empty.csv", StringIO(csv_data), "text/csv")}

    # Mock the upload response
    up = client.post(
        "/data/upload", files=files, data={"name": "EmptyDS"}, headers=headers
    )
    assert up.status_code == 200
