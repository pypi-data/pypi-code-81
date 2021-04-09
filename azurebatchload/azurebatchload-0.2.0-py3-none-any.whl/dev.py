# flake8: noqa
import time
import os
from azurebatchload import UploadBatch
from azurebatchload.download import DownloadBatch
from azurebatchload.utils import Utils
import pandas as pd

from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)


x = Utils(container="test").list_blobs()
print(x)