import os
import glob
import logging
import datetime as dt
import shutil
from typing import Set
from typeguard import typechecked


TEMP_BUCKET_NAME = "temp_file_upload"


def _get_path(bucket_name, file_path) -> str:
    root_dir = os.path.join(os.environ["LOCAL_STORAGE_PATH"], bucket_name)
    return os.path.join(root_dir, file_path)


@typechecked
def upload_blob(bucket_name: str, destination_blob_name: str, file_like_object):
    """
    writes files to local filesystem instead of cloud storage. Intended for local dev usage
    Also publishes a message to pubsub using the
    topic_name <bucket-name>-updates as a convention (emulating storage notifications)
    """
    logging.info(f"Writing file={destination_blob_name} to local filesystem")
    _, filename = os.path.split(destination_blob_name)

    # Appending microsecond timestamp to filename for uniqueness in temp folder
    file_path = _get_path(TEMP_BUCKET_NAME, filename + dt.datetime.now().strftime('_%H_%M_%S_%f'))
    logging.debug(f"Writing first to a temporary location {file_path}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as file:
        shutil.copyfileobj(file_like_object, file)

    destination_path = _get_path(bucket_name, destination_blob_name)
    logging.debug(f"Moving to final destination {destination_path}")
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    os.rename(file_path, destination_path)


@typechecked
def list_blobs(bucket_name: str, prefix: str) -> Set[str]:
    """Lists files from local filesystem instead of cloud storage. Intended for local dev usage. Should imitate
    Google's list_blobs cloud storage function"""
    path = _get_path(bucket_name, prefix)
    paths = glob.glob(path + '*', recursive=True)

    logging.info(f"Found {len(paths)} existing files in local directory {path}")

    return set(os.path.split(path)[1] for path in paths)


def blob_exists(bucket_name: str, partial_file_path: str) -> bool:
    logging.info(f"Checking if file={partial_file_path} exists in dir={bucket_name}")
    # partial_file_path can also be a full file name, the glob will work correctly
    path = _get_path(bucket_name, f'{partial_file_path}*')
    return any(os.path.isfile(file) for file in glob.glob(path))


@typechecked
def download_blob(bucket_name: str, source_blob_name: str, file_like_object):
    path = _get_path(bucket_name, source_blob_name)
    logging.info(f"Reading local file {path}")
    with open(path, "rb") as file:
        shutil.copyfileobj(file, file_like_object)
    return file_like_object


@typechecked
def delete_blob(bucket_name: str, destination_blob_name: str):
    file_path = _get_path(bucket_name, destination_blob_name)
    logging.info(f"Deleting file={file_path} from local filesystem")
    os.remove(file_path)
