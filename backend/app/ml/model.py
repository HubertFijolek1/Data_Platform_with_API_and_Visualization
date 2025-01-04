import tensorflow as tf
from tensorflow import keras
import pandas as pd
from .preprocessing import preprocess_data
from sklearn.metrics import accuracy_score, precision_score, recall_score

def train_model(df: pd.DataFrame, label_column: str, epochs: int = 5) -> keras.Model:
    """
    Train a simple classification model using TensorFlow Keras.

    :param df: Pandas DataFrame containing the data.
    :param label_column: Name of the column in df that is the label.
    :param epochs: Number of epochs to train.
    :return: Trained Keras model.
    """
    # Preprocess the data
    df = preprocess_data(df)

    # Separate features & labels
    y = df[label_column].values
    X = df.drop(columns=[label_column]).values

    # For simplicity, assume all features are numeric already:
    # Build a simple feed-forward network
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(X.shape[1],)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')  # Example: binary classification
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # Train the model
    model.fit(X, y, epochs=epochs, batch_size=32, verbose=1)

    return model

def evaluate_model(model: keras.Model, df: pd.DataFrame, label_column: str):
    """
    Evaluate a trained Keras model on a dataset.
    Returns a dictionary of metrics: accuracy, precision, recall
    """
    df = preprocess_data(df)
    y_true = df[label_column].values
    X = df.drop(columns=[label_column]).values
    y_pred_probs = model.predict(X)
    # For binary classification, threshold=0.5
    y_pred = (y_pred_probs >= 0.5).astype(int)

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec
    }