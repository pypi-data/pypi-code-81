
import torch.nn as nn
import torchvision

def create_model(model_name, pretrained, n_classes):
    if model_name == "resnet18":
        model = torchvision.models.resnet18(pretrained=pretrained)
        model.fc = nn.Linear(model.fc.in_features, n_classes)

    return model