import boto3
import json

from os.path import expanduser


def connect_s3(credential):
    """
    Connect to S3 by using credential

    Args:
        credential (dict): mest have key_id and access_key

    Outputs:
        boto3.client
    """
    return boto3.client(
        's3',
        aws_access_key_id=credential["key_id"],
        aws_secret_access_key=credential["access_key"]
    )
