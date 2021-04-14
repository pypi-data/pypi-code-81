"""
Defines an abstract class model pytorch model defined with LightningModule
"""


from abc import abstractmethod

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader


class TorchModel(pl.LightningModule):

    """A `pytorch` based deep learning model or layer."""

    def __init__(self, **kwargs):
        super().__init__()
        self.lr = kwargs.get("lr", 1e-3)
        self.kwargs = kwargs
        """Define your model here.
        self.model = Sequential(nn.Linear(),....)
        """

    @abstractmethod
    def forward(self, x):
        """Define your forward pass here."""

    @abstractmethod
    def training_step(self, batch, batch_idx):
        """Define your `pytorch` training loop."""

    def configure_optimizers(self):
        """(Optional) Configure training optimizers."""

        return torch.optim.Adam(self.parameters(), lr=self.lr)

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader = None,
        epochs: int = 10,
        **kwargs
    ):
        """Fit a model to data.

        Without overloading (necessary for adjusting architectures to
        variable DataLoaders), `TorchModel` can still train with this base
        implementation.
        """
        self.trainer = pl.Trainer(max_epochs=epochs, **kwargs)
        self.trainer.fit(self, train_loader, val_loader)

    def predict(self, x):
        """Run inference on data.

        TODO: implementation...

        """
        return self.forward(x)
