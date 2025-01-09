import pytest
from dotenv import load_dotenv
import os


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Fixture to load environment variables from the root .env file before any tests run.
    """
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
    )
    load_dotenv(dotenv_path=env_path)
