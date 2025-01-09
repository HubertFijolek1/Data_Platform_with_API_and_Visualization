import json
import logging
import os

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        extra="forbid",  # Ensures no unexpected fields are allowed
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v):
        logger.info(f"Received BACKEND_CORS_ORIGINS: {v}")
        if not v:
            logger.info("No CORS origins provided. Using default empty list.")
            return []
        if isinstance(v, str):
            # Attempt to parse as JSON list
            try:
                parsed = json.loads(v)
                logger.info(f"Parsed CORS origins as JSON: {parsed}")
                return parsed
            except json.JSONDecodeError:
                logger.warning(
                    "Failed to parse CORS origins as JSON. Falling back to "
                    "comma-separated string."
                )
                # Fallback to comma-separated string
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            logger.info(f"CORS origins already a list: {v}")
            return v
        logger.error("Invalid format for BACKEND_CORS_ORIGINS")
        raise ValueError("Invalid format for BACKEND_CORS_ORIGINS")

    @property
    def effective_database_url(self) -> str:
        """
        Determines which database URL to use based on the environment.
        Prioritizes TEST_DATABASE_URL if set.
        """
        if os.getenv("TEST_DATABASE_URL"):
            logger.info("Using TEST_DATABASE_URL for database connections.")
            return self.TEST_DATABASE_URL
        logger.info("Using DATABASE_URL for database connections.")
        return self.DATABASE_URL


settings = Settings()
