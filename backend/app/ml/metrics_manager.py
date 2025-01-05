"""
A simple in-memory storage for model performance metrics.
In a production environment, you'd likely store these in a DB or logging system.
"""

metrics_store = {}  # dict with keys: (model_name, version), value: dict of metrics

def save_metrics(model_name: str, version: str, metrics: dict):
    metrics_store[(model_name, version)] = metrics

def get_metrics(model_name: str, version: str):
    return metrics_store.get((model_name, version), None)
