import tensorflow as tf
from tensorflow import keras
import pandas as pd
from .preprocessing import preprocess_data


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
