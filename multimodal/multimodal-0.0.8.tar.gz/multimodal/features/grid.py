from pySmartDL import SmartDL
from multimodal import DEFAULT_DATA_DIR
import os

class COCOJiangGridFeatures:

    name = "jiang-grid-feats"

    urls = {
        "X-152++": "https://dl.fbaipublicfiles.com/grid-feats-vqa/X-152pp/X-152pp-features.tgz",
        "X-152": "https://dl.fbaipublicfiles.com/grid-feats-vqa/X-152/X-152-features.tgz",
        "X-101": "https://dl.fbaipublicfiles.com/grid-feats-vqa/X-101/X-101-features.tgz",
        "R-50": "https://dl.fbaipublicfiles.com/grid-feats-vqa/R-50/R-50-features.tgz",
    }

    def __init__(self, version="X-152++", dir_data=None) -> None:
        self.version = version
        dir_data = dir_data or DEFAULT_DATA_DIR
        self.dir_features = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_features, exist_ok=True)
        self.featspath = os.path.join(self.dir_features, f"{self.version}.tables")

        if not os.path.exists(self.featspath):
            path_download = self._download()
            self._process_file(path_download)
        

    def _download(self):
        url = self.urls[self.features_name]
        dl = SmartDL(url, self.dir_data)
        destination = dl.get_dest()
        if not os.path.exists(dl.get_dest()):
            dl.start()
        return destination

    def _process_file(path_download):
        pass

    def __getitem__(self, image_id):
        pass
