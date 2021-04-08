from pathlib import Path

import requests
from deepchainapps import log


def _create_download_folder() -> Path:
    """create .deepchain folder if not exist"""
    path = Path.home().joinpath(".cache")
    path.mkdir(exist_ok=True)

    path.joinpath("deepchain-apps").joinpath("data")
    path.mkdir(exist_ok=True)

    return path

class Downloader:
    def __init__(self,file_uri):
        self.file_uri = file_uri

    def download(self):
        r = requests.


