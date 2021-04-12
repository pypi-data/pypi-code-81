# Copy from https://github.com/thuml/Transfer-Learning-Library
from typing import Optional
import os

from gorilla2d.datasets import ImageList, download_data, check_exits


class Office31(ImageList):
    """Office31 Dataset.

    Parameters:
        - **root** (str): Root directory of dataset
        - **task** (str): The task (domain) to create dataset. Choices include ``'A'``: amazon, \
            ``'D'``: dslr and ``'W'``: webcam.
        - **download** (bool, optional): If true, downloads the dataset from the internet and puts it \
            in root directory. If dataset is already downloaded, it is not downloaded again.
        - **transform** (callable, optional): A function/transform that  takes in an PIL image and returns a \
            transformed version. E.g, ``transforms.RandomCrop``.
        - **target_transform** (callable, optional): A function/transform that takes in the target and transforms it.

    .. note:: In `root`, there will exist following files after downloading.
        ::
            amazon/
                images/
                    backpack/
                        *.jpg
                        ...
            dslr/
            webcam/
            image_list/
                amazon.txt
                dslr.txt
                webcam.txt
    """
    download_list = [
        ("image_list", "image_list.zip", "https://cloud.tsinghua.edu.cn/f/1f5646f39aeb4d7389b9/?dl=1"),
        ("amazon", "amazon.tgz", "https://cloud.tsinghua.edu.cn/f/05640442cd904c39ad60/?dl=1"),
        ("dslr", "dslr.tgz", "https://cloud.tsinghua.edu.cn/f/a069d889628d4b468c32/?dl=1"),
        ("webcam", "amazon.tgz", "https://cloud.tsinghua.edu.cn/f/4c4afebf51384cf1aa95/?dl=1"),
    ]
    aliases = {
        "amazon": ["amazon", "Amazon", "a", "A"],
        "webcam": ["webcam", "Webcam", "w", "W"],
        "dslr": ["dslr", "Dslr", "d", "D"],
    }
    image_list = {
        "amazon": "image_list/amazon.txt",
        "webcam": "image_list/webcam.txt",
        "dslr": "image_list/dslr.txt",
    }
    classes = ['back_pack', 'bike', 'bike_helmet', 'bookcase', 'bottle', 'calculator', 'desk_chair', 'desk_lamp',
               'desktop_computer', 'file_cabinet', 'headphones', 'keyboard', 'laptop_computer', 'letter_tray',
               'mobile_phone', 'monitor', 'mouse', 'mug', 'paper_notebook', 'pen', 'phone', 'printer', 'projector',
               'punchers', 'ring_binder', 'ruler', 'scissors', 'speaker', 'stapler', 'tape_dispenser', 'trash_can']

    def __init__(self,
                 root: str,
                 task: str,
                 download: Optional[bool] = False,
                 **kwargs):
        for name, alias in self.aliases.items():
            if task in alias:
                task = name
                break
        assert task in self.image_list
        data_list_file = os.path.join(root, self.image_list[task])

        if download:
            list(map(lambda args: download_data(root, *args), self.download_list))
        else:
            list(map(lambda args: check_exits(root, args[0]), self.download_list))

        super().__init__(root, Office31.classes, data_list_file=data_list_file, **kwargs)
