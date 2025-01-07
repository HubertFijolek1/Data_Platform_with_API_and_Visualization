import logging.config
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse

from .routers import auth_router, data_router, predict_router, ml_ops_router, data_generator_router, data_upload_router
from .config.settings import settings

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

# CORS configuration using centralized settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(data_router)
app.include_router(predict_router)
app.include_router(ml_ops_router)
app.include_router(data_generator_router)
app.include_router(data_upload_router)

@app.get("/test-logging")
def test_logging():
    logger.info("Testing INFO log level.")
    logger.debug("Testing DEBUG log level.")
    return {"message": "Logs have been written to console or file."}

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=429)