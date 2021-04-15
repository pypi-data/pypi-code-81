import torch.nn as nn  # neural networks

from TTS.tts.layers.generic.wavenet import WNBlocks


class WNSpecEncoder(nn.Module):
    """Encodes input spectrograms into queries
    TODO: handle multi-speaker case"""

    def __init__(self, in_channels, out_channels, c_in_channels=None):
        super().__init__()

        self.in_layer = nn.Conv1d(in_channels, out_channels, 1)

        self.wn_blocks = WNBlocks(
            out_channels,
            out_channels,
            kernel_size=3,
            dilation_rate=3,
            num_blocks=2,
            num_layers=4,
            c_in_channels=c_in_channels,
            dropout_p=0,
            weight_norm=False,
        )
        self.out_layer = nn.Conv1d(out_channels, out_channels, 1)

    def forward(self, x):
        """TODO: add x_mask for masking paddings"""
        o = nn.functional.relu(self.in_layer(x))
        o = self.wn_blocks(o)
        o = self.out_layer(o)
        return o
