import logging.config
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from .config.settings import settings
from .routers import (
    auth_router,
    data_generator_router,
    data_router,
    data_upload_router,
    ml_ops_router,
)

load_dotenv()

# Load logging config from a file
LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), "../logging.conf")
if os.path.exists(LOGGING_CONFIG):
    logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
else:
    # Fallback to basicConfig if logging.conf not found
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("app")

app = FastAPI(
    title="Data Analysis Platform API",
    description="""
This API allows you to manage and analyze datasets.
""",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Analysis Platform API"}


# CORS configuration using centralized settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(data_upload_router)
app.include_router(data_router)
app.include_router(ml_ops_router)
app.include_router(data_generator_router)

uploads_dir = os.path.join(os.getcwd(), "uploads")
os.makedirs(uploads_dir, exist_ok=True)  # Creates the directory if it doesn't exist

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


async def get_ml_prediction(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://backend-ml:8000/predict/", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error, possibly raise an HTTPException
            raise HTTPException(
                status_code=response.status_code, detail="ML prediction failed"
            )


@app.get("/test-logging")
def test_logging():
    logger.info("Testing INFO log level.")
    logger.debug("Testing DEBUG log level.")
    return {"message": "Logs have been written to console or file."}


@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=429)
