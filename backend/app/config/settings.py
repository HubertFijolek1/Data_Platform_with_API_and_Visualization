import os
import json
import logging
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator, ValidationError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
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
                logger.warning("Failed to parse CORS origins as JSON. Falling back to comma-separated string.")
                # Fallback to comma-separated string
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            logger.info(f"CORS origins already a list: {v}")
            return v
        logger.error("Invalid format for BACKEND_CORS_ORIGINS")
        raise ValueError("Invalid format for BACKEND_CORS_ORIGINS")


settings = Settings()
