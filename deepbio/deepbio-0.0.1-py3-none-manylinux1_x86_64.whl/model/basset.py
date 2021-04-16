"""
Basset
~~~

Basset was originally trained on a compendium of accessible genomic sites
mapped in 164 cell types by DNaseI-seq. Basset predictions for the change in
accessibility between two variant alleles.

While a computational approach to annotate and interpret the noncoding genome,
Basset also offers a flexible convolutional architecture for a wide range of
genomic prediction and motif implication tasks.

@article {Kelley028399,
    author = {Kelley, David R. and Snoek, Jasper and Rinn, John L.},
    title = {Basset: Learning the regulatory code of the accessible genome with deep convolutional neural networks},
    elocation-id = {028399},
    year = {2015},
    doi = {10.1101/028399},
    publisher = {Cold Spring Harbor Laboratory},
    URL = {https://www.biorxiv.org/content/early/2015/10/05/028399},
    eprint = {https://www.biorxiv.org/content/early/2015/10/05/028399.full.pdf},
    journal = {bioRxiv}
}
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from deepbio.model import TorchModel
from deepbio.data import DataLoader
import pytorch_lightning as pl


class Basset(TorchModel):

    """Basset is a flexible convolutional architecture for genomic prediction."""

    def __init__(self):
        super(Basset, self).__init__()

        # TODO: input dim should be parameter
        self.input = nn.Linear(1344, 1344)

        self.conv_block1 = nn.Sequential(
            nn.Conv1d(4, 288, 17), nn.BatchNorm1d(288), nn.MaxPool1d(3)
        )

        def _construct_conv_tower(num_blocks, num_filters, filter_multiplier):
            """Utility function to construct stack of compatible conv layers."""
            conv_tower = []
            for i in range(num_blocks):
                new_filters = int(num_filters * filter_multiplier)
                conv_tower.append(
                    nn.Sequential(
                        nn.Conv1d(num_filters, new_filters, 5),
                        nn.BatchNorm1d(new_filters),
                        nn.MaxPool1d(2),
                    )
                )
                num_filters = new_filters
            return conv_tower

        self.conv_tower = _construct_conv_tower(6, 288, 1.122)

        self.conv_block2 = nn.Sequential(
            nn.Conv1d(572, 256, 1), nn.BatchNorm1d(256))

        self.dense1 = nn.Sequential(
            nn.Linear(512, 768), nn.BatchNorm1d(1), nn.Dropout(0.2)
        )
        self.dense2 = nn.Linear(768, 164)

    def forward(self, x):

        # TODO: implement stochastic_shift over residue frame to reduce overfit

        # (batch, 4, 1344)
        x, is_rc = self._stochastic_reverse_complement(self.input(x))
        x = F.gelu(x)

        # (batch, 4, 1344)
        x = self.conv_block1(x)

        # (batch, 288, 442)
        for conv_block in self.conv_tower:
            x = F.gelu(conv_block(x))

        # (batch, 2, 572)
        x = F.gelu(self.conv_block2(x))

        # (batch, 256, 2)
        x = torch.unsqueeze(torch.flatten(x, start_dim=1), dim=1)

        # (batch, 1, 512)
        x = F.gelu(self.dense1(x))
        # (batch, 1, 768)
        x = torch.sigmoid(self.dense2(x))

        # (batch, 1, 164)
        return x

    def training_step(self, batch, batch_idx):
        """Defines a pytorch training loop.

        TODO: typing

        Args:
            batch: Tuple containing sample and label (opt.) pair.
            batch_idx: Batch index in an epoch.
        """
        x, y = batch

        y_hat = self.forward(torch.tensor(x).float())
        y = torch.unsqueeze(y, 0).float()
        loss = F.binary_cross_entropy(y_hat, y)
        return loss

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

    def configure_optimizers(self):
        """(Optional) Configure training optimizers."""

        return torch.optim.SGD(self.parameters(), lr=0.005, momentum=0.98)

    def _stochastic_shift(self, seq: torch.tensor):
        """Apply short nucleotide frame shift at random.

        TODO: types
        """
        pass

    def _stochastic_reverse_complement(self, seq: torch.tensor):
        """Randomly convert a one-hot encoded sequence to its reverse complement.

        TODO: types
        """

        # Assume OHE follows [A, C, G, T].
        # Constructs OHE reverse complement as you would expect...
        idx = (
            torch.tensor([3, 2, 1, 0])
            .reshape(4, 1)
            .repeat(seq.shape[0], 1, seq.shape[-1])
        )
        rc = torch.gather(seq, 1, idx)
        rc = torch.flip(rc, [-1])

        return (rc, True) if torch.rand(1) > 0.5 else (seq, False)
