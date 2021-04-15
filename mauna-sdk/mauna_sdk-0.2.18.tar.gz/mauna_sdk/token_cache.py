import os
import fcntl
import hashlib
import tempfile
from contextlib import contextmanager, suppress
from datetime import datetime


@contextmanager
def file_lock(fd, cmd):
    try:
        fcntl.lockf(fd, cmd)
        yield
    except IOError:
        yield
    finally:
        fcntl.lockf(fd, fcntl.LOCK_UN)


class TokenCache:
    def __init__(self, dev_id, api_key):
        self._hash = hashlib.md5(f"{dev_id}:{api_key}".encode()).hexdigest()

    @property
    def cache_path(self):
        ts = int(
            datetime.now()
            .replace(minute=0)
            .replace(second=0)
            .replace(microsecond=0)
            .timestamp()
        )
        return os.path.join(tempfile.gettempdir(), f"mauna-{self._hash}-{ts}")

    def read(self):
        with suppress(FileNotFoundError):
            with open(self.cache_path, "r") as f:
                with file_lock(f, fcntl.LOCK_SH):
                    return f.read()

    def write(self, data):
        with open(self.cache_path, "a") as f:
            with file_lock(f, fcntl.LOCK_EX):
                f.seek(0)
                f.truncate(0)
                f.write(data)
