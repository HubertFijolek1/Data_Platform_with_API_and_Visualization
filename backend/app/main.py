from fastapi import FastAPI
from .routers import auth, data
from .middlewares import error_handling_middleware

app = FastAPI(
    title="Data Analysis Platform API",
    description="""
This API allows you to manage and analyze datasets, including:
- **User authentication and registration** 
- **Dataset upload, retrieval, deletion** 
- **Role-based access control** (admin/user)
""",
    version="1.0.0",
)

# Register custom middleware for error handling (see below)
app.middleware("http")(error_handling_middleware)

app.include_router(auth.router)
app.include_router(data.router)
