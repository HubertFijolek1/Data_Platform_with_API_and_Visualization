import os
import subprocess
import sys
from urllib.parse import urlparse

import psycopg2
import pytest
from alembic import command
from alembic.config import Config
from app.database import get_db
from app.main import app
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Fixture to load environment variables from the root .env file before any tests run.
    """
    # Adjust path to your actual .env if needed
    env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
    load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Fixture to create the test database before any tests run.
    """
    script_path = os.path.join(
        os.path.dirname(__file__), "../../scripts/create_test_db.py"
    )
    subprocess.run([sys.executable, script_path], check=True)
    yield
    # Teardown: Drop the test database after tests
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/data_db_test",
    )
    parsed = urlparse(TEST_DATABASE_URL)
    dbname = parsed.path[1:]
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port

    try:
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {dbname};")
        print(f"Test database '{dbname}' dropped successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error dropping test database: {e}")


@pytest.fixture(scope="session")
def db_engine():
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/data_db_test",
    )
    engine = create_engine(TEST_DATABASE_URL)

    # Apply Alembic migrations
    alembic_cfg = Config(
        os.path.join(os.path.dirname(__file__), "../../../alembic.ini")
    )
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield engine


@pytest.fixture(scope="session")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="session")
def client(db_session):
    """
    Provide a FastAPI test client, overriding the DB dependency with our test session.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_token(client: TestClient):
    """
    Create a user + login to produce a Bearer token for tests.
    """
    # Register user
    reg_resp = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert reg_resp.status_code == 200, reg_resp.text

    # Login
    login_resp = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert login_resp.status_code == 200, login_resp.text
    return login_resp.json()["access_token"]
