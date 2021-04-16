import os, logging
from kolibri.settings import DATA_PATH
from kolibri.data.auto_downloader import DownloaderBase

LOGGER = logging.getLogger(__name__)

class Ressources(DownloaderBase):

    def __init__(self):
        """

        """
        super().__init__(
            download_dir=DATA_PATH)

    def get(self, resource_path):
        self.download(resource_path)
        self.path=os.path.join(DATA_PATH, resource_path)
        return self


resources=Ressources()