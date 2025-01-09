"""
Example script for automatically training models offline.
Could be triggered via cron, Docker, or external scheduling.
"""

import os
import sys
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.app.ml.model import train_model, save_model, evaluate_model


def main():
    # For demonstration, load some CSV from an external path:
    data_path = os.path.join(PROJECT_ROOT, "sample_data", "classification_data.csv")
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}, cannot train.")
        sys.exit(1)

    df = pd.read_csv(data_path)
    label_column = "label"
    model_name = "auto_trained_model"
    version = "v1"

    # Train a model
    model = train_model(df, label_column=label_column, epochs=3)
    # Save the model
    save_path = save_model(model, model_name, version=version)
    print(f"Model saved to {save_path}")

    # Evaluate and store metrics
    metrics = evaluate_model(model, df, label_column=label_column)
    print(f"Metrics: {metrics}")
    from backend.app.ml.metrics_manager import save_metrics

    save_metrics(model_name, version, metrics)

    print("Automated training completed successfully.")


if __name__ == "__main__":
    main()
