import hashlib
import pathlib
import urllib.request
import zipfile

import numpy as np
import tqdm
import yaml


def tqdm_hook(t: tqdm.tqdm):
    """Wraps tqdm progress bar to provide update hook method for `urllib.urlretrieve`."""
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


def get_data(root_folder: str, url: str, md5: str = None) -> pathlib.Path:
    """Download and unzip the data if it is not already present in root_folder."""
    root_folder = pathlib.Path(root_folder)

    data_folder = root_folder / "data"
    if not data_folder.is_dir():
        data_folder.mkdir()
    data_zip = data_folder / "tensile_tests.zip"
    if not data_zip.exists():
        with tqdm.tqdm(desc="Downloading tensile test data files", unit="bytes", unit_scale=True) as t:
            reporthook = tqdm_hook(t)
            urllib.request.urlretrieve(url, data_zip, reporthook=reporthook)
        if md5:
            if not validate_checksum(data_zip, md5):
                raise AssertionError("MD5 does not match: Zip file is corrupt. Delete zip file and retry download.")
            else:
                print("MD5 validated. Download complete.")
        with zipfile.ZipFile(data_zip, 'r') as zip_ref:
            zip_ref.extractall(data_folder)
    return data_folder


def validate_checksum(file_path: pathlib.Path, valid_md5: str) -> bool:
    with open(file_path, 'rb') as binary_zip:
        md5_hash = hashlib.md5()
        md5_hash.update(binary_zip.read())
        digest = md5_hash.hexdigest()
        if digest == valid_md5:
            return True
        else:
            return False


def load_tensile_data(Test_analysed: str, data_folder: pathlib.Path):
    """Load data from files into a NumPy array."""
    experiment_folder = data_folder / f'test {Test_analysed}/displacement data/'
    data_files = list(experiment_folder.glob("*.csv"))
    Nb_images = np.shape(data_files)[0] - 1
    empty_file = 0  # To manage empty files
    Data = []
    for i in range(Nb_images):
        data = np.loadtxt(data_files[i], delimiter=',', comments='x')

        if np.shape(data)[0] == 0:
            empty_file += 1
        else:
            Data.append(data)
    Nb_images = Nb_images - empty_file
    return Data, Nb_images


def read_data_yaml(data_yaml_path: str) -> dict:
    path = pathlib.Path(data_yaml_path)
    with open(path) as file:
        return yaml.load(file, Loader=yaml.SafeLoader)
