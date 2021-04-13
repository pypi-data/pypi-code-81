from huggingface_hub import ModelHubMixin
from torch import nn

from .configuration_resnet import ResnetConfig
from .resnet import BasicBlock, Bottleneck, ResNet

RESNET_BLOCK_TYPE_MAP = {"bottleneck": Bottleneck, "basic": BasicBlock}


RESNET_PRETRAINED_TORCHVISION_URL_MAP = {
    "resnet18": "https://download.pytorch.org/models/resnet18-5c106cde.pth",
    "resnet34": "https://download.pytorch.org/models/resnet34-333f7ec4.pth",
    "resnet50": "https://download.pytorch.org/models/resnet50-19c8e357.pth",
    "resnet101": "https://download.pytorch.org/models/resnet101-5d3b4d8f.pth",
    "resnet152": "https://download.pytorch.org/models/resnet152-b121ed2d.pth",
    "resnext50_32x4d": "https://download.pytorch.org/models/resnext50_32x4d-7cdf4587.pth",
    "resnext101_32x8d": "https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth",
    "wide_resnet50_2": "https://download.pytorch.org/models/wide_resnet50_2-95faca4d.pth",
    "wide_resnet101_2": "https://download.pytorch.org/models/wide_resnet101_2-32ee1156.pth",
}

RESNET_PRETRAINED_TORCHVISION_CONFIG_MAP = {
    "resnet18":  ResnetConfig(block="basic", layers=[2, 2, 2, 2]),
    "resnet34": ResnetConfig(block="basic", layers=[3, 4, 6, 3]),
    "resnet50": ResnetConfig(block="bottleneck", layers=[3, 4, 6, 3]),
    "resnet101": ResnetConfig(block="bottleneck", layers=[3, 4, 23, 3]),
    "resnet152": ResnetConfig(block="bottleneck", layers=[3, 8, 36, 3]),
    "resnext50_32x4d": ResnetConfig(block="bottleneck", layers=[3, 4, 6, 3], groups=32, width_per_group=4),
    "resnext101_32x8d": ResnetConfig(block="bottleneck", layers=[3, 4, 23, 3], groups=32, width_per_group=8),
    "wide_resnet50_2": ResnetConfig(block="bottleneck", layers=[3, 4, 6, 3], width_per_group=128),
    "wide_resnet101_2": ResnetConfig(block="bottleneck", layers=[3, 4, 23, 3], width_per_group=128),
}


class ResnetPreTrainedModel(nn.Module, ModelHubMixin):

    config_class = ResnetConfig
    base_model_prefix = "resnet"

    def __init__(self, *args, **kwargs):
        super().__init__()


class ResnetModel(ResnetPreTrainedModel):
    def __init__(self, config: ResnetConfig, **kwargs):
        super().__init__()
        self.config = ResnetConfig(**config) if isinstance(config, dict) else config
        block = RESNET_BLOCK_TYPE_MAP.get(self.config.block)
        if block is None:
            raise RuntimeError("Block must be either 'bottleneck' or 'basic-block'")

        self.resnet = ResNet(
            block=block,
            layers=self.config.layers,
            num_labels=self.config.num_labels,
            zero_init_residual=self.config.zero_init_residual,
            groups=self.config.groups,
            width_per_group=self.config.width_per_group,
            replace_stride_with_dilation=self.config.replace_stride_with_dilation,
            norm_layer=self.config.norm_layer,
        )
        self.config.output_size = list(self.resnet.modules())[-4].weight.size(0)

    def forward(self, x):
        return self.resnet(x)
