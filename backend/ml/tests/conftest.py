from unittest.mock import MagicMock

import pytest


@pytest.fixture
def client():
    mock_client = MagicMock()
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.text = "OK"
    mock_client.post.return_value = mock_post_response
    return mock_client


@pytest.fixture
def auth_token():
    return "mocked_auth_token"
