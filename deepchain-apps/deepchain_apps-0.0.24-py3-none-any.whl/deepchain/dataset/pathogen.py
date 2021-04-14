"""
Load the pathogen dataset available at :
    https://storage.googleapis.com/deepchain-datasets-public/pathogen.pkl
"""
import numpy as np
import pandas as pd

from .downloader import Downloader
from .utils import RemoteFileData

REMOTE_PATHOGEN = RemoteFileData(
    filename="pathogen.pkl",
    url="https://storage.googleapis.com/deepchain-datasets-public/pathogen.pkl",
)


def load_pathogen_dataset(with_sequence: bool = False) -> pd.DataFrame:
    """
    Download and load dataset from public bucket
    Store data in ~/.cache/deepchain-apps/data
    Data contains 3 columns:
        - sequence: str
        - sequence_id: str
        - class: str
        - protbert_embedding= np.array

    Arguments
    ---------
    with_sequence -> bool : if True, return the raw sequence in addition
                            if False, only embedding and class

    """
    downloader = Downloader(REMOTE_PATHOGEN)
    downloader.fetch_remote()
    pathogen = pd.read_pickle(downloader.local_file)

    sequence = pathogen["sequence"].to_numpy()
    X = np.asarray(pathogen["protbert_embedding"].tolist())
    y = pathogen["class"].to_numpy()

    if with_sequence:
        return X, y, sequence
    else:
        return X, y
