"""
Define a generic MLP for training
Uses to learn model from embedding

Example:
    from deepchainapps.models import MLP
    from deepchainps.data import TorchDataloader

    mlp = MLP()
    dl = TorchDataoader(X,y)
    mlp.fit(dl)
"""


import torch
import torch.nn.functional as F
from torch import nn

from .torch_model import TorchModel


class MLP(TorchModel):
    """Multi-layer perceptron model."""

    def __init__(self, input_shape: int = 768):
        super().__init__()
        self._model = nn.Sequential(
            nn.Linear(input_shape, 128), nn.ReLU(), nn.Linear(128, 1), nn.Sigmoid()
        )

    def forward(self, x):
        """Defines forward pass"""
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x).float()
        return self._model(x)

    def training_step(self, batch, batch_idx):
        """training_step defined the train loop. It is independent of forward"""
        x, y = batch
        y_hat = self._model(x)
        y = torch.unsqueeze(y, 1)
        loss = F.binary_cross_entropy(y_hat, y)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def save_model(self, path: str):
        """Save entire model with torch"""
        torch.save(self._model, path)
