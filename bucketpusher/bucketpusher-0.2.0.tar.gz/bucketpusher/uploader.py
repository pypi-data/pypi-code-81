from dataclasses import dataclass, field
import os
import threading
import pathlib
import time
from google.cloud import storage
import concurrent.futures as cf
from loguru import logger
from typing import Optional, Union
from . import auth
from . import exceptions
from . import utils


@dataclass
class UploadStatus:
    filepath: pathlib.Path
    time_started: float = field(default_factory=time.time)
    time_complete: float = 0
    size: int = 0
    bytes_so_far: int = 0
    total_bytes: int = 0
    num_uploaded: int = 0
    num_files: int = 0
    num_errors: int = 0
    num_skipped: int = 0
    complete: bool = False

    def done(self) -> None:
        self.time_complete = time.time()
        self.complete = True

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.time_started


class Uploader:
    def __init__(
        self,
        bucket_id: Optional[str],
        service_account_file: Optional[pathlib.Path],
        user_credentials_path: Optional[pathlib.Path],
        key: Optional[Union[str, bytes]],
        client_secrets_path: Optional[pathlib.Path],
        dry_run: bool,
        prefix: Optional[str],
        delete_files_after_upload: bool,
    ) -> None:

        self._stop = False
        self._thread = None
        self.dry_run = dry_run
        self.futures = None
        self.delete_files_after_upload = delete_files_after_upload
        self.lock = threading.Lock()

        if prefix:
            self.prefix = prefix.rstrip("/") + "/"
        else:
            self.prefix = ""

        if bucket_id is not None and len(bucket_id) < 3:
            raise ValueError("Must provide a valid bucket ID")
        self.bucket_id = bucket_id

        self.client = None

        service_account_file = (
            pathlib.Path(service_account_file)
            if service_account_file
            else pathlib.Path("")
        )

        credentials = None

        service_account_file = (
            pathlib.Path(service_account_file)
            if service_account_file is not None
            else None
        )
        user_credentials_path = (
            pathlib.Path(user_credentials_path)
            if user_credentials_path is not None
            else None
        )
        client_secrets_path = (
            pathlib.Path(client_secrets_path)
            if client_secrets_path is not None
            else None
        )
        try:
            if (
                isinstance(user_credentials_path, pathlib.Path)
                and user_credentials_path.is_file()
            ):
                logger.debug(f"Using {user_credentials_path}")
                credentials = auth.unpickle_user_credentials(user_credentials_path, key)
            elif (
                isinstance(service_account_file, pathlib.Path)
                and service_account_file.is_file()
            ):
                logger.debug(f"Using {service_account_file}")
                credentials, bucket = auth.unpickle_service_account_credentials(
                    service_account_file, key, True
                )
                self.bucket_id = bucket if self.bucket_id is None else self.bucket_id
            elif (
                isinstance(client_secrets_path, pathlib.Path)
                and client_secrets_path.is_file()
            ):
                logger.debug(f"Running auth flow with {client_secrets_path}")
                credentials = self.run_oauth_flow(
                    user_credentials_path, client_secrets_path, key
                )
            self.client = storage.Client(project=None, credentials=credentials)
        except Exception:
            logger.exception("Authentication error")
            raise ValueError("Authentication failed")

    @staticmethod
    def run_oauth_flow(user_credentials_path, client_secrets_path, key):
        credentials = auth.get_credentials_via_client_secrets_file(
            client_secrets_path, key
        )
        auth.pickle_user_credentials(credentials, user_credentials_path, key)
        return credentials

    def start(
        self,
        paths,
        callback=lambda x: None,
    ):

        if not (paths and all([pathlib.Path(_).exists() for _ in paths])):
            raise ValueError("Must provide valid paths to files or folders")

        self._stop = False

        try:
            bucket = self.client.bucket(self.bucket_id)
        except Exception:
            logger.exception("Failed to instantiate bucket")
            raise Exception("Failed to connect as invalid destination URI")

        self._thread = threading.Thread(
            target=self._future_handler,
            args=(bucket, paths, callback),
            daemon=True,
        )
        self._thread.start()

    def _future_handler(self, bucket, paths, callback):

        self.futures = {}

        job = self._mock_upload if self.dry_run else self._upload

        self._upload_status = UploadStatus(None)

        max_workers = max(os.cpu_count() - 1, 2)
        with cf.ThreadPoolExecutor(max_workers=max_workers) as executor:

            for path, dest in utils.parse_paths(paths):
                if self._stop:
                    break

                size = path.stat().st_size

                # Start accumulating sizes for running stats
                with self.lock:
                    self._upload_status.total_bytes += size
                    self._upload_status.num_files += 1

                self.futures[
                    executor.submit(
                        job,
                        path,
                        (pathlib.Path(self.prefix) / dest).as_posix(),
                        bucket,
                        callback,
                    )
                ] = path

        self._upload_status.done()
        callback(self._upload_status)

    @property
    def active(self):
        if self._thread is not None and self._thread.is_alive():
            return True
        return False

    def stop(self):
        self._stop = True
        if self.futures:
            [_.cancel() for _ in self.futures.keys() if not _.done()]

    def _upload(self, path, dest, bucket, cb):
        if self._stop:
            return
        skipped = num_errors = False
        try:
            blob = bucket.blob(str(dest))
            blob.upload_from_filename(str(path), checksum="crc32c")
            logger.info(f"Uploaded {path} to {dest}")
        except Exception as e:
            if exceptions.is_delete_permission_error(e):
                logger.warning(f"{path} already exists on the remote")
                skipped = True
            else:
                logger.exception(f"Error attempting uploading {path}")
                num_errors = True

        with self.lock:
            if skipped or num_errors:
                self._upload_status.num_skipped += 1
                self._upload_status.num_errors += 1
            else:
                self._upload_status.num_uploaded += 1
                self._upload_status.bytes_so_far += path.stat().st_size
                if self.delete_files_after_upload:
                    logger.info(f"Deleting {path}")
                    path.unlink()
            self._upload_status.filepath = path
            cb(self._upload_status)

    def _mock_upload(self, path, dest, bucket, cb):
        if self._stop:
            return
        time.sleep(1)
        with self.lock:
            self._upload_status.num_uploaded += 1
            self._upload_status.bytes_so_far += path.stat().st_size
            cb(self._upload_status)
