import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "somepassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"

    # Duplicate email
    response2 = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "newuser@example.com",
            "password": "anotherpass",
        },
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"

    # Duplicate username
    response3 = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "third@example.com",
            "password": "anotherpass",
        },
    )
    assert response3.status_code == 400
    assert response3.json()["detail"] == "Username already taken"


def test_login_user(client: TestClient):
    # Must have a user to login
    reg = client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword",
        },
    )
    assert reg.status_code == 200

    # Good login
    resp = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "loginpassword",
        },
    )
    assert resp.status_code == 200
    token_data = resp.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Wrong password
    resp_wrong = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "WRONGpass",
        },
    )
    assert resp_wrong.status_code == 401
    assert resp_wrong.json()["detail"] == "Invalid credentials"

    # Non-existent user
    resp_non = client.post(
        "/auth/login",
        json={
            "email": "nobody@example.com",
            "password": "nopassword",
        },
    )
    assert resp_non.status_code == 401
    assert resp_non.json()["detail"] == "Invalid credentials"
