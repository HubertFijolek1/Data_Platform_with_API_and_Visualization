from .predict import router as predict_router
from .predict2 import router as predict2_router
from .train import router as train_router
from .train2 import router as train2_router

__all__ = [
    "train_router",
    "predict_router",
    "train2_router",
    "predict2_router",
]
