import torch
import torch.nn as nn
import torchvision.models as models


class RecognitionModel(nn.Module):
    def __init__(self):
        super(RecognitionModel, self).__init__()
        self.bottom = models.mobilenet_v2(True, progress=True)
        self.bottom = self.bottom.features
        for params in self.bottom.parameters():
            params.requires_grad = False
        self.top = nn.Sequential(
            nn.Linear(in_features=1280*4*4, out_features=256),
            nn.ReLU(),
            nn.Linear(in_features=256, out_features=2),
            nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        x = self.bottom(x)
        x = x.view((x.shape[0], -1))
        x = self.top(x)
        return x
