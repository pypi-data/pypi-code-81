
from pathlib import Path

import boto3
from botocore.errorfactory import ClientError

from uchu.aws.s3 import S3

class Space(S3):
    def __init__(self, region_name, access_key_id, secret_access_key):
        self.region_name = region_name
        self.endpoint_url = f"https://{self.region_name}.digitaloceanspaces.com"
        # Get a key from:
        # https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = boto3.session.Session()
        self._client = self.session.client('s3', region_name=region_name,
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key)
