from unittest.mock import MagicMock

import pytest
from app.crud.crud import create_user, verify_password
from app.schemas.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def mock_db_session():
    return MagicMock()


def test_create_user(mock_db_session):
    user_in = UserCreate(
        username="unittest_user",
        email="unittest@example.com",
        password="unittest_password",
    )

    # Mock session
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    created_user = create_user(mock_db_session, user_in)

    assert created_user.username == "unittest_user"
    assert created_user.email == "unittest@example.com"
    # Check password hashing
    assert verify_password("unittest_password", created_user.hashed_password)


def test_verify_password():
    hashed = pwd_context.hash("mysecret")
    assert verify_password("mysecret", hashed) is True
    assert verify_password("notsecret", hashed) is False
