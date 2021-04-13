import os
import shutil
import h5py
from pySmartDL import SmartDL

from multimodal import DEFAULT_DATA_DIR
from multimodal.utils import download_and_unzip


def get_basename(url):
    return url.split("/")[-1]


class H5Reader:
    pass


class GQAVGFeatures:

    name = "gqa-vg"

    urls = {
        "spatial": "https://nlp.stanford.edu/data/gqa/spatialFeatures.zip",
        "objects": "https://nlp.stanford.edu/data/gqa/objectFeatures.zip",
    }

    def __init__(self, features="spatial", dir_data=None):
        self.features = features

        if dir_data is None:
            dir_data = DEFAULT_DATA_DIR

        self.dir_feats = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_feats, exist_ok=True)

        if self.dir_data is None:
            self.dir_data = DEFAULT_DATA_DIR
        self.download()

    def download(self):
        url = self.urls[self.features]
        dir_dest = self.dir_feats
        download_and_unzip(url, dir_dest)

    def __getitem__(self, image_id: int) -> dict:
        pass
