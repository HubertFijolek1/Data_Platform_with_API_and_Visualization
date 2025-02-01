metrics_store = {}  # dict with keys: (model_name, version), value: dict of metrics


def save_metrics(model_name: str, version: str, metrics: dict):
    metrics_store[(model_name, version)] = metrics


def get_metrics(model_name: str, version: str):
    return metrics_store.get((model_name, version), None)
