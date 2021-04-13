# Modify from https://github.com/thuml/Transfer-Learning-Library
import os
import numpy as np
from typing import Optional, Callable, Tuple, List, Dict
import torchvision.datasets as datasets
from torchvision.datasets.folder import default_loader

from gorilla.config import Config


class ImageList(datasets.VisionDataset):
    r"""Author: zhang.haojian
    A generic Dataset class for domain adaptation in image classification

    Args:
    root (str): Root directory of dataset
    classes (List[str]): The names of all the classes
    data_list_file (str): File to read the image list from
    transform (callable, optional): A function/transform that  takes in an PIL image
        and returns a transformed version. E.g, ``transforms.RandomCrop``
    target_transform (callable, optional): A function/transform that takes in the target
        and transforms it
    cfg (Config, optional): Config of the experiment

    .. note:: In `data_list_file`, each line 2 values in the following format.
        ::
            source_dir/dog_xxx.png 0
            source_dir/cat_123.png 1
            target_dir/dog_xxy.png 0
            target_dir/cat_nsdf3.png 1

        The first value is the relative path of an image, and the second value is the label of the corresponding image.
        If your data_list_file has different formats, please over-ride `parse_data_file`.
    """

    def __init__(self,
                 root: str,
                 classes: List[str],
                 data_list_file: str,
                 transform: Optional[Callable] = None,
                 target_transform: Optional[Callable] = None,
                 **kwargs):
        # currently kwargs is only used to receive 'cfg' params to be compatible
        # with Digit dataset
        super().__init__(root, transform=transform, target_transform=target_transform)
        self.paths, self.targets = self.parse_data_file(data_list_file)
        self.classes = classes
        self.class_to_idx = {cls: idx
                             for idx, clss in enumerate(self.classes)
                             for cls in clss}
        self.loader = default_loader

    def __getitem__(self, index: int) -> Dict:
        """
        Parameters:
            - **index** (int): Index
            - **return** (tuple): (image, target) where target is index of the target class.
        """
        path, target = self.paths[index], self.targets[index]
        img = self.loader(path)
        item = {}
        if self.transform is not None:
            if isinstance(self.transform, dict):
                for key, transform in self.transform.items():
                    item.update({key: transform(img)})
            else:
                img = self.transform(img)
                item.update({"img": img})

        if self.target_transform is not None and target is not None:
            target = self.target_transform(target)

        item.update({"target": target, "path": path})
        return item

    def __len__(self) -> int:
        return len(self.paths)

    def parse_data_file(self, file_name: str) -> List[Tuple[str, int]]:
        """Parse file to data list

        Parameters:
            - **file_name** (str): The path of data file
            - **return** (list): List of (image path, class_index) tuples
        """
        with open(file_name, "r") as f:
            paths, targets = [], []
            for line in f.readlines():
                path, target = line.split()
                if not os.path.isabs(path):
                    path = os.path.join(self.root, path)
                paths.append(path)
                targets.append(int(target))
        return paths, np.array(targets)

    @property
    def num_classes(self) -> int:
        """Number of classes"""
        return len(self.classes)
