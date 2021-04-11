import boto3


def get_param(key, region_name: str = "eu-west-1"):
    ssm = boto3.client("ssm", region_name=region_name)
    parameter = ssm.get_parameter(Name=key, WithDecryption=True)
    return parameter["Parameter"]["Value"]
