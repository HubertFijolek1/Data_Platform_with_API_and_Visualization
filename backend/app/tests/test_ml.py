import pytest
import pandas as pd
import torch

from ..ml.model import train_model, evaluate_model
from ..ml.pytorch_model import train_pytorch_classifier
from ..ml.sentiment import SentimentAnalyzer

@pytest.fixture
def dummy_classification_data():
    # Create a small DataFrame for testing classification
    df = pd.DataFrame({
        "feature1": [0.1, 0.2, 0.9, 1.0],
        "feature2": [1.2, 0.3, 0.5, 0.4],
        "label": [0, 0, 1, 1]
    })
    return df

def test_tensorflow_training(dummy_classification_data):
    model = train_model(dummy_classification_data, label_column="label", epochs=1)
    metrics = evaluate_model(model, dummy_classification_data, label_column="label")
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0.0

def test_pytorch_training(dummy_classification_data):
    model = train_pytorch_classifier(dummy_classification_data, label_column="label", epochs=1)
    X = dummy_classification_data.drop(columns=["label"]).values
    X_torch = torch.tensor(X, dtype=torch.float32)
    with torch.no_grad():
        preds = model(X_torch)
    assert preds.shape[0] == len(dummy_classification_data)

def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer()
    texts = ["I love this!", "This is terrible."]
    results = analyzer.batch_analyze(texts)
    assert len(results) == 2
    # First should have positive polarity, second negative
    assert results[0]["polarity"] > 0
    assert results[1]["polarity"] < 0
