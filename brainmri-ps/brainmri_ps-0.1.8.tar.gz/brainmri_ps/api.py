import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_path)

import torch
import torch.nn as nn
import albumentations as A
import albumentations.pytorch as AT
import gdown

from data import BrainMRIDataset
from models import create_model
from utils import dcm2image, study2series_dict

__all__ = ['PulseSequenceClassifier']

model_urls = {
    'mobilenet_v2': '1P7mR3RkGEIqbANmzqVXvU1Kwr4qXKgeq',}


class PulseSequenceClassifier():
    def __init__(self, model_name="mobilenet_v2", device="cpu"):
        self.device = torch.device(device)

        self.model_name = model_name

        supported_models = list(model_urls.keys())
        if model_name not in supported_models:
            raise NotImplementedError('Currently supported models are', list(model_urls.keys()))

        self.model = create_model(self.model_name, pretrained=False, n_classes=7)
        self.model = self.model.to(self.device)
        self.model = nn.DataParallel(self.model)

        self.transform = A.Compose([
            A.Resize(256, 256),
            A.Normalize(),
            AT.ToTensor()
        ])

        self.label_dict = dict([
            (0, "FLAIR"),
            (1, "T1C"),
            (2, "T2"),
            (3, "ADC"),
            (4, "DWI"),
            (5, "TOF"),
            (6, "OTHER"),
        ])

    def from_pretrained(self):
        checkpoint_path = module_path + "/{}.pt".format(self.model_name)
        if not os.path.exists(checkpoint_path):
            checkpoint_url = f'https://drive.google.com/uc?id={model_urls[self.model_name]}'
            gdown.cached_download(checkpoint_url, checkpoint_path)
        self.model.load_state_dict(torch.load(checkpoint_path, map_location=self.device))
        return self

    def predict_instance(self, instance_path):
        image = dcm2image(instance_path)
        image = self.transform(image=image)["image"]

        with torch.no_grad():
            self.model.eval()
            image = image.unsqueeze(0).to(self.device)

            output = self.model(image)
            pred = torch.max(output, 1)[1].detach().cpu().numpy()

        return self.label_dict[pred[0]]

    def predict_study(self, study_path):
        self.series_dict = study2series_dict(study_path)
        self.loader = torch.utils.data.DataLoader(
            BrainMRIDataset(
                self.series_dict,
                image_transform=self.transform
            ),
            batch_size=len(self.series_dict), shuffle=False
        )

        with torch.no_grad():
            self.model.eval()
            series_uids, images = next(iter(self.loader))
            images = images.to(self.device)

            outputs = self.model(images)
            preds = torch.max(outputs, 1)[1].detach().cpu().numpy()

        for i, series_uid in enumerate(series_uids):
            self.series_dict[series_uid] = self.label_dict[preds[i]]

        return self.series_dict
