import boto3
import datetime

from s3transfer import S3UploadFailedError
from s3fs import S3FileSystem
from airflow_commons.logger import LOGGER


def get_param(key, region_name: str = "eu-west-1"):
    ssm = boto3.client("ssm", region_name=region_name)
    parameter = ssm.get_parameter(Name=key, WithDecryption=True)
    return parameter["Parameter"]["Value"]


def upload_file_to_s3_bucket(path_to_file: str, bucketname: str, filename: str):
    """
    Uploads the given file to the given s3 bucket.

    :param path_to_file: Path to file that will be uploaded to s3 bucket.
    :param bucketname: Name of the bucket that file will be uploaded to.
    :param filename: Name of the file (key of the file in s3).
    """
    LOGGER("Upload to " + bucketname + " started")
    upload_start = datetime.now()
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(path_to_file, bucketname, filename)
    except S3UploadFailedError as e:
        LOGGER("Upload to " + bucketname + " failed")
        raise Exception(e)
    upload_end = datetime.now()
    LOGGER(
        (
            "Upload finished in ",
            round((upload_end - upload_start).total_seconds()),
            " seconds",
        )
    )


def write_into_s3_file(
    bucketname: str, filename: str, data: str, key: str = None, secret: str = None
):
    """
    Writes the given string data into the specified file in the specified bucket. If file does not exists create one, if
    exists overrides it. If the aws key and secret is not given, method uses the environmental variables as credentials.

    :param bucketname: Name of the bucket that the target file is stored
    :param filename: Name of the file that will be overridden
    :param data: A string contains the content of the file
    :param key: AWS access key id, default is None
    :param secret: AWS secret access key, default is None
    """
    if key is not None and secret is not None:
        s3 = S3FileSystem(key=key, secret=secret)
    else:
        s3 = S3FileSystem()

    LOGGER("Writing to " + bucketname + "/" + filename + " started")
    writing_start = datetime.now()
    if s3.ls(bucketname):
        with s3.open(bucketname + "/" + filename, "w") as f:
            f.write(data)
    else:
        raise Exception("Bucket does not exists")
    writing_end = datetime.now()
    LOGGER(
        (
            "Writing finished in ",
            round((writing_end - writing_start).total_seconds()),
            " seconds",
        )
    )
