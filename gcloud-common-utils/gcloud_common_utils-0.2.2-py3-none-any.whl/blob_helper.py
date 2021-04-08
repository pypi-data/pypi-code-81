import logging
from io import IOBase
from typing import Set

from google.cloud import storage
from nivacloud_logging.log_utils import LogContext
from typeguard import typechecked


@typechecked
def upload_blob(bucket_name: str, destination_blob_name: str, file_like_object):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    with LogContext(bucket_name=bucket_name, destination_blob_name=destination_blob_name):
        logging.info("Attempting to upload file")
        bucket = storage_client.bucket(bucket_name)
        new_blob = bucket.blob(destination_blob_name)
        new_blob.upload_from_file(file_like_object)
        logging.info("File uploaded completed")


@typechecked
def list_blobs(bucket_name: str, prefix: str) -> Set[str]:
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket_list = bucket.list_blobs(prefix=prefix)
    # Get the file list from the google cloud bucket, store in a set
    bucket_file_set = set()
    for blob in bucket_list:
        bucket_file_set.add(blob.name.rsplit('/', 1)[1] if '/' in blob.name else blob.name)

    logging.info(f'{len(bucket_file_set)} files found in cloud bucket {bucket_name} with prefix "{prefix}"',
                 extra={'bucket_file_count': len(bucket_file_set),
                        'bucket_name': bucket_name, 'prefix': prefix})

    return bucket_file_set


def blob_exists(bucket_name: str, partial_file_path: str) -> bool:
    """partial_file_path will also correctly match if a full file path is supplied"""
    storage_client = storage.Client()
    logging.info('Checking if file exists', extra={'bucket_name': bucket_name, 'file_path': partial_file_path})
    bucket = storage_client.bucket(bucket_name)
    return any(bucket.list_blobs(prefix=partial_file_path, delimiter='/'))


@typechecked
def download_blob(bucket_name: str, source_blob_name: str, file_like_object):
    storage_client = storage.Client()
    logging.info('Downloading file', extra={'file': source_blob_name, 'bucket_name': bucket_name})
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_file(file_like_object)
    logging.info('Blob file was downloaded', extra={'file': source_blob_name})
    return file_like_object


@typechecked
def delete_blob(bucket_name: str, source_blob_name: str):
    storage_client = storage.Client()
    logging.info('Deleting file', extra={'file': source_blob_name, 'bucket_name': bucket_name})
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.delete()
    logging.info("Blob deleted")
