from fastapi.testclient import TestClient


def test_update_profile_success(client: TestClient, auth_token: str):
    """
    1) Use the 'auth_token' fixture -> user is testuser@example.com
    2) Update the user's email & password
    3) Confirm 200 + "Profile updated successfully."
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    params = {"email": "updated_email@example.com", "password": "NewSecretPassword"}
    resp = client.put("/auth/update_profile", params=params, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Profile updated successfully."


def test_update_profile_email_conflict(client: TestClient, auth_token: str):
    """
    If we attempt to set an email that already belongs to another user, expect 400 "Email already registered..."
    """
    # 1) Create a second user with known email
    r2 = client.post(
        "/auth/register",
        json={
            "username": "AnotherUser",
            "email": "existing@example.com",
            "password": "somepass",
        },
    )
    assert r2.status_code == 200

    # 2) Now from the first user, try to update to "existing@example.com"
    headers = {"Authorization": f"Bearer {auth_token}"}
    params = {"email": "existing@example.com"}
    r3 = client.put("/auth/update_profile", params=params, headers=headers)
    assert r3.status_code == 400
    assert "Email already registered" in r3.text


def test_update_profile_no_changes(client: TestClient, auth_token: str):
    """
    If no query params are provided, we expect "No changes made."
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.put("/auth/update_profile", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "No changes made."


def test_update_profile_unauthenticated(client: TestClient):
    """
    If no token is supplied, expect 401
    """
    r = client.put("/auth/update_profile", params={"email": "willfail@example.com"})
    assert r.status_code == 401
    assert "Could not validate credentials" in r.text
