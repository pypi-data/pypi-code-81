import torch.nn as nn
import torchvision


def create_model(model_name, pretrained, n_classes):
    model = None
    if model_name == "resnet18":
        model = torchvision.models.resnet18(pretrained=pretrained)
        model.fc = nn.Linear(model.fc.in_features, n_classes)
    if model_name == "mobilenet_v2":
        model = torchvision.models.mobilenet_v2(pretrained=pretrained)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, n_classes)

    return model
