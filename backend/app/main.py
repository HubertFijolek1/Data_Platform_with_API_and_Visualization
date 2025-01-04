import logging
import logging.config
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, data
from .middlewares import error_handling_middleware
from .utils.rate_limiter import limiter

# load logging config from a file
LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), "..", "logging.conf")
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

# Register the custom error-handling middleware
app.middleware("http")(error_handling_middleware)

# Add the rate limiting middleware from "slowapi" or a custom solution (see below).
app.add_middleware(limiter._middleware_class, limiter=limiter)

app.include_router(auth.router)
app.include_router(data.router)

# Example usage in routes (pseudocode):
@app.get("/test-logging")
def test_logging():
    logger.info("Testing INFO log level.")
    logger.debug("Testing DEBUG log level.")
    return {"message": "Logs have been written to console or file."}
