"""Defines a generic model ABCs.

Interfaces provided are intended to be extended by developers for custom
use-cases.
"""

from abc import abstractmethod

import torch
from torch import nn
import torch.nn.functional as F
import pytorch_lightning as pl

from deepbio.data import DataLoader


class TorchModel(pl.LightningModule):

    """A `pytorch` based deep learning model or layer.

    The core philosophy with DeepBio `TorchModel` extensions is flexibility
    and un-opinionated interfaces.

    Developers should freely design architectures and training logic in native
    pytorch without framework lock-in. SOTA architectures, especially, have
    many moving pieces that are impossible to account for __a priori__.
    """

    def __init__(self):
        super().__init__()
        """Define your model here.

        Put whatever you need (losses, metrics, sub-models, etc.) to implement
        the `TorchModel` interface.
        """

    @abstractmethod
    def forward(self, x):
        """Define your forward pass here."""

    @abstractmethod
    def training_step(self, batch, batch_idx):
        """Define your `pytorch` training loop."""

    def configure_optimizers(self):
        """(Optional) Configure training optimizers."""

        return torch.optim.Adam(self.parameters(), lr=1e-3)

    def fit(
        self, train_loader: DataLoader, val_loader: DataLoader = None, epochs: int = 10
    ):
        """Fit a model to data.

        Without overloading (necessary for adjusting archiectures to
        variable DataLoaders), `TorchModel` can still train with this base
        implementation.
        """

        trainer = pl.Trainer(max_epochs=epochs)
        trainer.fit(self, train_loader, val_loader)

    def predict(self, x):
        """Run inference on data.

        TODO: implementation...

        """
        x = self._dataloader._featurizer(x)
        return self.forward(x)


class Model(object):
    """ABC for generic DeepBio Model."""

    def __init__(self):

        raise NotImplementedError

    @abstractmethod
    def fit(self):

        raise NotImplementedError

    @abstractmethod
    def predict(self):

        raise NotImplementedError


class SciKitModel(object):
    """ABC for generic DeepBio Model."""

    def __init__(self):

        raise NotImplementedError

    @abstractmethod
    def fit(self):

        raise NotImplementedError

    @abstractmethod
    def predict(self):

        raise NotImplementedError
