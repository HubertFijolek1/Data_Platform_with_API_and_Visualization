from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/ml", tags=["metrics"])

# In-memory store for example
metrics_store = {}


@router.get("/metrics/{model_name}/{version}")
def get_metrics(model_name: str, version: str):
    # If no metrics found, raise 404 or return empty
    if (model_name, version) not in metrics_store:
        raise HTTPException(status_code=404, detail="No metrics found.")
    return metrics_store[(model_name, version)]
