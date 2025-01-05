import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from .preprocessing import preprocess_data

class SimplePyTorchModel(nn.Module):
    def __init__(self, input_dim, hidden_dim=16):
        super(SimplePyTorchModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)  # Example: single output for binary classification

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

def train_pytorch_classifier(df: pd.DataFrame, label_column: str, epochs=5):
    """
    Train a simple PyTorch model for binary classification using CPU (example).
    """
    df = preprocess_data(df)
    y = df[label_column].values
    X = df.drop(columns=[label_column]).values

    # Convert numpy arrays to torch tensors
    X_torch = torch.tensor(X, dtype=torch.float32)
    y_torch = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    model = SimplePyTorchModel(input_dim=X.shape[1])
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_torch)
        loss = criterion(outputs, y_torch)
        loss.backward()
        optimizer.step()

        if (epoch+1) % 1 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    return model
