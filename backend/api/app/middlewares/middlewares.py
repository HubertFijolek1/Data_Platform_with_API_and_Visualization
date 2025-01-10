import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def error_handling_middleware(request: Request, call_next):
    """
    Middleware to handle unexpected errors or log them in a specific way.
    """
    try:
        return await call_next(request)
    except HTTPException as exc:
        # HTTPExceptions are re-raised as is, so they appear as intended
        raise exc
    except Exception:
        # Log the actual traceback somewhere (e.g., logger, external service)
        print("UNEXPECTED ERROR:", traceback.format_exc())

        # Return a generic 500 response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error. Please try again later."},
        )
