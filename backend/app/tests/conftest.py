import pytest
from dotenv import load_dotenv
import os
import sys
import subprocess
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.database import Base, get_db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse

# Add the project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
sys.path.insert(0, PROJECT_ROOT)

from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Fixture to load environment variables from the root .env file before any tests run.
    """
    env_path = os.path.join(PROJECT_ROOT, ".env")
    load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Fixture to create the test database before any tests run.
    """
    # Run the database creation script
    script_path = os.path.join(PROJECT_ROOT, "scripts", "create_test_db.py")
    subprocess.run([sys.executable, script_path], check=True)
    yield
    # Teardown: Drop the test database after tests
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/data_db_test",
    )
    url = urlparse.urlparse(TEST_DATABASE_URL)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

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
    alembic_cfg = Config(os.path.join(PROJECT_ROOT, "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield engine

    # Teardown: Drop all tables (handled in create_test_database fixture)


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
    # Override the get_db dependency to use the testing session
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
    # Register a test user
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200

    # Login the test user
    response = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
