import os
import cv2
from glob import glob
from tqdm import tqdm
import numpy as np
import shutil

FOLDER_NAME = "DATA/"


def __is_picture(file):
    """
    It returns whether the processed file is a jpg picture or not.
    All arguments must be of equal length.
    :param file: longitude of first place
    :return: A boolean indicating whether the file is a jpg image or not
    """
    if file.lower().endswith("jpg") or file.lower().endswith("jpeg"):
        return True
    else:
        return False


def __unzip_folders(path):
    """
    It unzips all the the compressed files inside a directory
    and removes the zipped folders
    :param zip_name: a folder
    :return: None
    """
    print("Unzipping folders...")
    # Unzip folders
    all_zip_files = os.listdir(path)
    for zip_file in all_zip_files:
        if zip_file != ".DS_Store":
            shutil.unpack_archive(zip_file)
            break

    print("Removing ZIP folders...")
    # Remove Zipped folders
    all_files = os.listdir(".")
    for file_name in all_files:
        if file_name.endswith("zip"):
            os.remove(path + file_name)


def load_datasets(path="./", im_size=(128, 128)):
    """
    High-level function for creating Numpy Arrays from Zip Files
    :param path: path where the zip files are stored
    :param im_size: Image size of the loaded picures. Width and height
    must be positive.
    :return: Numpy arrays for both the images (X) and the labels (y)
    =========
    Example:
    =========
    X, y = load_datasets(".", (256, 256))
    """
    if im_size[0] <= 0 or im_size[1] <= 0:
        return -1

    __unzip_folders(path)

    print("Loading Datasets...")
    # Create index for transform labels into class numbers
    tag2idx = {tag.split("/")[1]: i for i, tag in enumerate(glob(path + "*"))}
    im_path = path + "*/*"
    print("Loading data...")

    # Create X array from images with OpenCV
    X = np.array(
        [
            cv2.resize(cv2.imread(file_path), im_size)
            for file_path in tqdm(glob(im_path))
            if __is_picture(file_path)
        ]
    )
    # Create y array from index
    y = [
        tag2idx[file_path.split("/")[1]]
        for file_path in glob(im_path)
        if __is_picture(file_path)
    ]
    # Transform y array into a categorical array
    y = np.eye(len(np.unique(y)))[y].astype(np.uint8)

    return X, y
