from .auth import router as auth_router
from .data import router as data_router
from .predict import router as predict_router
from .ml_ops import router as ml_ops_router

__all__ = ["auth_router", "data_router", "predict_router", "ml_ops_router"]