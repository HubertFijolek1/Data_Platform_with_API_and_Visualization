from fastapi import FastAPI
from .routers import auth, data

app = FastAPI()

app.include_router(auth.router)
app.include_router(data.router)
