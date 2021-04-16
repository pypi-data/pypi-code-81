import errno
import json
import os
from pathlib import Path


class IOUtils:

    @staticmethod
    def read_dict_from_file(file):
        try:
            with open(file, 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            raise e

    @staticmethod
    def read_file(file):
        file_path = Path(file)
        if not file_path.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        with open(file, 'r') as f:
            return f.read()
