from unittest.mock import MagicMock

import pytest


@pytest.fixture
def client():
    """
    Mocked TestClient fixture for ML tests.
    This mock client simulates API interactions.
    """
    mock_client = MagicMock()

    # Define a mock response for POST requests to /data/upload
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.text = "OK"

    # When client.post(...) is called, return the mock response
    mock_client.post.return_value = mock_post_response

    return mock_client


@pytest.fixture
def auth_token():
    """
    Mocked authentication token.
    """
    return "mocked_auth_token"
