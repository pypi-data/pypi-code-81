# Copyright (c) Gorilla-Lab. All rights reserved.
from typing import Optional, Dict
import os

import numpy as np
from torch.utils.data import Dataset
from torchvision.transforms import Compose, Resize, ToTensor, Normalize, Lambda, RandomCrop
from torchvision.datasets import MNIST, SVHN, USPS

from gorilla.config import Config


class Digit(Dataset):
    r"""Author: zhang.haojian
    Digit Dataset.

    Args:
    root (str): Root directory of dataset
    task (str): The task (domain) to create dataset.
    download (bool, optional): If true, downloads the dataset from the internet and puts
        it in root directory. If dataset is already downloaded, it is not downloaded again.
    cfg (Config, optional): Config of the experiment

    note: In `root`, there will exist following files after downloading:
        MNIST/
            raw/
            processed/  [60000, 28, 28], [10000, 28, 28]
        usps/
            usps.bz2  [7291, 16, 16]
            usps.t.bz2  [2007, 16, 16]
        svhn/
            train_32x32.mat  [73257, 32, 32]
            test_32x32.mat  [26032, 32, 32]
    """
    aliases = {
        "mnist": ["mnist", "MNIST", "mt", "m", "M"],
        "usps": ["usps", "USPS", "up", "u", "U"],
        "svhn": ["svhn", "SVHN", "sv", "s", "S"],
    }
    data_folders = {
        "mnist": "./",
        "usps": "usps/",
        "svhn": "svhn/",
    }
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self,
                 root: str,
                 task: str,
                 transform: Dict,
                 download: Optional[bool] = False,
                 cfg: Config = None,
                 **kwargs):
        # currently kwargs is only used to receive 'transform' params to be compatible
        # with ImageList dataset
        for name, alias in self.aliases.items():
            if task in alias:
                task = name
                break
        assert task in self.data_folders
        usps = "usps" in [cfg.source, cfg.target]
        all_use = cfg.get("all_use", True)

        root = os.path.join(root, self.data_folders[task])
        if task == cfg.source:
            _transform = transform[task][cfg.target]
        else:
            _transform = transform[task][cfg.source]

        if task == "mnist":
            self.dataset = MNIST(root,
                                 train=cfg.train_set,
                                 transform=_transform,
                                 download=download)
            if usps and cfg.train_set and not all_use:
                indices = np.random.permutation(self.dataset.data.shape[0])[:2000]
                self.dataset.data = self.dataset.data[indices, :, :]
                self.dataset.targets = np.array(self.dataset.targets)[indices]

        elif task == "usps":
            self.dataset = USPS(root,
                                train=cfg.train_set,
                                transform=_transform,
                                download=download)
            if cfg.train_set and not all_use:
                indices = np.random.permutation(self.dataset.data.shape[0])[:1800]
                self.dataset.data = self.dataset.data[indices, :, :]
                self.dataset.targets = np.array(self.dataset.targets)[indices]

        elif task == "svhn":
            self.dataset = SVHN(root,
                                split="train" if cfg.train_set else "test",
                                transform=_transform,
                                download=download)

        else:
            raise NotImplementedError("task {}".format(task))

    def __getitem__(self, idx) -> Dict:
        img, target = self.dataset[idx]
        # return 'path' key for compatibility of other Dataset
        return dict(img=img, target=target, path="")

    def __len__(self) -> int:
        return len(self.dataset)

    @property
    def num_classes(self) -> int:
        """Number of classes"""
        return len(self.classes)
