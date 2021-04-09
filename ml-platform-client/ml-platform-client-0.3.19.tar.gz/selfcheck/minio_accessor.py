import os
import traceback

import time
from minio import Minio


class MinIOAccessor:
    _client = None
    max_retry = 3

    def __init__(self, host, access_key, secret_key, secure):
        self.client = Minio(host, access_key=access_key, secret_key=secret_key, secure=secure)

    def fget_object(self, filepath: str, save_path: str):
        pos = filepath.index('/')
        bucket = filepath[:pos]
        filepath = filepath[pos + 1:]
        retry = 0
        while retry < MinIOAccessor.max_retry:
            try:
                self.client.fget_object(bucket, filepath, save_path)
                return
            except Exception as e:
                traceback.print_exc()
                retry += 1
                time.sleep(2)

    def save_object(self, local_path: str, remote_path: str):
        print('minio save object, local_path: {}, remote_path: {}'.format(local_path, remote_path))
        pos = remote_path.index('/')
        bucket = remote_path[:pos]
        filepath = remote_path[pos + 1:]
        with open(local_path, 'rb') as file_data:
            file_stat = os.stat(local_path)
            self.client.put_object(bucket, filepath, file_data, file_stat.st_size)

    def delete(self, bucket, prefix: str, recursive=False):
        objs = self.client.list_objects(bucket, prefix, recursive)
        for obj in objs:
            self.client.remove_object(bucket, obj.object_name)
