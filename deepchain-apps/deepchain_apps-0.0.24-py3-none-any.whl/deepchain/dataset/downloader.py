import urllib
from pathlib import Path

import requests
from deepchain import log

from .utils import RemoteFileData


class Downloader:
    """
    Base object to safely download data from google Cloud public repo
    The class need to ne initialize with a RemoteFileData object, which
    is basically a namedtuple:
        RemoteFileData:
            - filename
            - URL

    """

    def __init__(self, remote: RemoteFileData):
        self.remote = remote
        self.path_cache_data = self._create_download_folder()
        self.local_file = self.path_cache_data.joinpath(self.remote.filename)

    def fetch_remote(self):
        """
        Fetch data from a public url adress
        """
        if not self.local_file.is_file():
            try:
                log.info("Download file at : %s", self.remote.url)
                urllib.request.urlretrieve(self.remote.url, str(self.local_file))
            except:
                log.warning("Can't access to the public file %s", self.remote.url)

    def _create_download_folder(self) -> Path:
        """
        Create deepchain-apps folder in .cache if not exist
        """
        path = Path.home().joinpath(".cache", "deepchain-apps", "data")
        path.mkdir(exist_ok=True, parents=True)

        return path
