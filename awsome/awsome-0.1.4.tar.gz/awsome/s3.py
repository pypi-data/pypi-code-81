import boto3


class S3Client(object):
    def __init__(self, region, aws_key_id, aws_key_secret, bucket):
        self.client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_key_secret)
        self.region = region
        self.bucket = bucket

    def get_objects(self, prefix, max_keys=100, token=""):
        response = self.client.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix,
            MaxKeys=max_keys
        ) if token == "" else self.client.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix,
            MaxKeys=max_keys,
            ContinuationToken=token,
        )
        next_token = ""
        if "NextContinuationToken" in response.keys():
            # no next page of this query
            next_token = response["NextContinuationToken"]
        return response.get("Contents", []), next_token

    def get_file_data_by_key(self, key):
        return self.client.get_object(
            Bucket=self.bucket,
            Key=key)["Body"]._raw_stream.data

    def put_file_by_key(self, data_in_bytes, key):
        import io
        data = io.BytesIO(data_in_bytes)
        self.client.upload_fileobj(data, self.bucket, key)

    def ls(self, dir=""):
        if len(dir) != 0 and dir[-1] != "/":
            dir = dir+"/"
        prefixes = self.client.list_objects(
            Bucket=self.bucket, Delimiter="/", Prefix=dir).get("CommonPrefixes")
        subdirs = [prefix["Prefix"].replace(dir, "") for prefix in prefixes]
        return subdirs
