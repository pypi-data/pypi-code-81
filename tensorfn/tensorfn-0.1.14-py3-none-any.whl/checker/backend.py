from datetime import datetime
import io
import os
import functools
import sys

import torch
from termcolor import colored
from tabulate import tabulate

try:
    import boto3
    from tqdm import tqdm

except ImportError:
    boto3 = None


from tensorfn import distributed as dist, get_logger, nsml


def torch_serialize(obj):
    buf = io.BytesIO()
    torch.save(obj, buf)
    buf.seek(0)

    return buf.read()


class Storage:
    def checkpoint(self, obj, path):
        binary = torch_serialize(obj, path)
        self.save(binary, path)

    def get_directory(self, path):
        # dup = len(self.list(path)) + 1
        # path = f"{path}/{str(dup).zfill(5)}"
        key = datetime.now().astimezone().isoformat().replace(":", ".")
        path = f"{path}/{key}"

        return path


class Local(Storage):
    def __init__(self, path):
        root, child = os.path.split(path)
        if root == "":
            root = "."

        path = os.path.join(root, child)

        self.path = self.get_directory(path)

    def list(self, path):
        try:
            dirs = os.listdir(path)

        except FileNotFoundError:
            dirs = []

        return dirs

    def checkpoint(self, obj, name):
        target_path = os.path.join(self.path, name)
        os.makedirs(os.path.split(target_path)[0], exist_ok=True)

        torch.save(obj, os.path.join(self.path, name))

    def save(self, data, name):
        if isinstance(data, bytes):
            flag = "wb"

        else:
            flag = "w"

        target_path = os.path.join(self.path, name)

        os.makedirs(os.path.split(target_path)[0], exist_ok=True)

        with open(target_path, flag) as f:
            f.write(data)

    def load(self, name):
        pass


def progress_callback(pbar):
    def wrap(bytes_amount):
        pbar.update(bytes_amount)

    return wrap


class S3(Storage):
    def __init__(
        self, bucket, path, access_key, secret_key, endpoint=None, show_progress=True
    ):
        if boto3 is None:
            raise ImportError("boto3 should be installed for S3 storage")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
        )
        self.bucket = bucket
        self.path = self.get_directory(path)
        self.show_progress = show_progress

    def list(self, path):
        if path[-1] != "/":
            path += "/"

        resp = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=path, Delimiter="/")

        try:
            prefixes = []

            for prefix in resp["CommonPrefixes"]:
                prefixes.append(prefix["Prefix"])

        except KeyError:
            prefixes = []

        return prefixes

    def checkpoint(self, obj, name):
        buf = io.BytesIO()
        torch.save(obj, buf)
        size = buf.tell()
        buf.seek(0)

        self._save(buf, name, size)

    def save(self, data, name):
        buf = io.BytesIO(data)
        size = len(data)

        self._save(buf, name, size)

    def _save(self, buf, name, size):
        target_path = f"{self.path}/{name}"

        if self.show_progress:
            with tqdm(total=size, unit="B", unit_scale=True, desc=target_path) as pbar:
                self.s3.upload_fileobj(
                    buf, self.bucket, target_path, Callback=progress_callback(pbar)
                )

        else:
            self.s3.upload_fileobj(buf, self.bucket, target_path)


def default_formatter(step, **kwargs):
    panels = [f"step: {step}"]

    for k, v in kwargs.items():
        if isinstance(v, float):
            panels.append(f"{k}: {v:.3f}")

        else:
            panels.append(f"{k}: {v}")

    return "; ".join(panels)


class Logger:
    def __init__(self, formatter=None):
        if formatter is None:
            formatter = default_formatter

        self.logger = get_logger()
        self.formatter = formatter

    def log(self, step, **kwargs):
        self.logger.info(self.formatter(step, **kwargs))


class NSML:
    def log(self, step, **kwargs):
        nsml.report(summary=True, step=step, **kwargs)
