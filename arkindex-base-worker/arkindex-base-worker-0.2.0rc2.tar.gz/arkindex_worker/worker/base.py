# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
from pathlib import Path

import gnupg
import yaml
from apistar.exceptions import ErrorResponse
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex import ArkindexClient, options_from_env
from arkindex_worker import logger
from arkindex_worker.cache import create_tables, init_cache_db, merge_parents_cache


def _is_500_error(exc):
    """
    Check if an Arkindex API error is a 50x
    This is used to retry most API calls implemented here
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


class BaseWorker(object):
    def __init__(self, description="Arkindex Base Worker", use_cache=False):
        self.parser = argparse.ArgumentParser(description=description)

        # Setup workdir either in Ponos environment or on host's home
        if os.environ.get("PONOS_DATA"):
            self.work_dir = os.path.join(os.environ["PONOS_DATA"], "current")
        else:
            # We use the official XDG convention to store file for developers
            # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
            xdg_data_home = os.environ.get(
                "XDG_DATA_HOME", os.path.expanduser("~/.local/share")
            )
            self.work_dir = os.path.join(xdg_data_home, "arkindex")
            os.makedirs(self.work_dir, exist_ok=True)

        self.worker_version_id = os.environ.get("WORKER_VERSION_ID")
        if not self.worker_version_id:
            logger.warning(
                "Missing WORKER_VERSION_ID environment variable, worker is in read-only mode"
            )

        logger.info(f"Worker will use {self.work_dir} as working directory")

        self.use_cache = use_cache

    @property
    def is_read_only(self):
        """Worker cannot publish anything without a worker version ID"""
        return self.worker_version_id is None

    def configure(self):
        """
        Configure worker using cli args and environment variables
        """
        self.parser.add_argument(
            "-c",
            "--config",
            help="Alternative configuration file when running without a Worker Version ID",
            type=open,
        )
        self.parser.add_argument(
            "-d",
            "--database",
            help="Alternative SQLite database to use for worker caching",
            type=str,
            default=None,
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            help="Display more information on events and errors",
            action="store_true",
            default=False,
        )

        # Call potential extra arguments
        self.add_arguments()

        # CLI args are stored on the instance so that implementations can access them
        self.args = self.parser.parse_args()

        # Setup logging level
        if self.args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

        # Build Arkindex API client from environment variables
        self.api_client = ArkindexClient(**options_from_env())
        logger.debug(f"Setup Arkindex API client on {self.api_client.document.url}")

        # Load features available on backend, and check authentication
        user = self.request("RetrieveUser")
        logger.debug(f"Connected as {user['display_name']} - {user['email']}")
        self.features = user["features"]

        if self.worker_version_id:
            # Retrieve initial configuration from API
            worker_version = self.request(
                "RetrieveWorkerVersion", id=self.worker_version_id
            )
            logger.info(
                f"Loaded worker {worker_version['worker']['name']} revision {worker_version['revision']['hash'][0:7]} from API"
            )
            self.config = worker_version["configuration"]["configuration"]
            required_secrets = worker_version["configuration"].get("secrets", [])
        elif self.args.config:
            # Load config from YAML file
            self.config = yaml.safe_load(self.args.config)
            required_secrets = self.config.get("secrets", [])
            logger.info(
                f"Running with local configuration from {self.args.config.name}"
            )
        else:
            self.config = {}
            required_secrets = []
            logger.warning("Running without any extra configuration")

        # Load all required secrets
        self.secrets = {name: self.load_secret(name) for name in required_secrets}

        if self.args.database is not None:
            self.use_cache = True

        task_id = os.environ.get("PONOS_TASK")
        if self.use_cache is True:
            if self.args.database is not None:
                assert os.path.isfile(
                    self.args.database
                ), f"Database in {self.args.database} does not exist"
                self.cache_path = self.args.database
            elif task_id:
                cache_dir = os.path.join(os.environ.get("PONOS_DATA", "/data"), task_id)
                assert os.path.isdir(cache_dir), f"Missing task cache in {cache_dir}"
                self.cache_path = os.path.join(cache_dir, "db.sqlite")
            else:
                self.cache_path = os.path.join(os.getcwd(), "db.sqlite")

            init_cache_db(self.cache_path)
            create_tables()
        else:
            logger.debug("Cache is disabled")

        # Merging parents caches (if there are any) in the current task local cache, unless the database got overridden
        if self.use_cache and self.args.database is None and task_id is not None:
            task = self.request("RetrieveTaskFromAgent", id=task_id)
            merge_parents_cache(
                task["parents"],
                self.cache_path,
                data_dir=os.environ.get("PONOS_DATA", "/data"),
                chunk=os.environ.get("ARKINDEX_TASK_CHUNK"),
            )

    def load_secret(self, name):
        """Load all secrets described in the worker configuration"""
        secret = None

        # Load from the backend
        try:
            resp = self.request("RetrieveSecret", name=name)
            secret = resp["content"]
            logging.info(f"Loaded API secret {name}")
        except ErrorResponse as e:
            logger.warning(f"Secret {name} not available: {e.content}")

        # Load from local developer storage
        base_dir = Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser()
        path = base_dir / "arkindex" / "secrets" / name
        if path.exists():
            logging.debug(f"Loading local secret from {path}")

            try:
                gpg = gnupg.GPG()
                decrypted = gpg.decrypt_file(open(path, "rb"))
                assert (
                    decrypted.ok
                ), f"GPG error: {decrypted.status} - {decrypted.stderr}"
                secret = decrypted.data.decode("utf-8")
                logging.info(f"Loaded local secret {name}")
            except Exception as e:
                logger.error(f"Local secret {name} is not available as {path}: {e}")

        if secret is None:
            raise Exception(f"Secret {name} is not available on the API nor locally")

        # Parse secret payload, according to its extension
        _, ext = os.path.splitext(os.path.basename(name))
        try:
            ext = ext.lower()
            if ext == ".json":
                return json.loads(secret)
            elif ext in (".yaml", ".yml"):
                return yaml.safe_load(secret)
        except Exception as e:
            logger.error(f"Failed to parse secret {name}: {e}")

        # By default give raw secret payload
        return secret

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(self, *args, **kwargs):
        """
        Proxy all Arkindex API requests with a retry mechanism
        in case of 50X errors
        The same API call will be retried 5 times, with an exponential sleep time
        going through 3, 4, 8 and 16 seconds of wait between call.
        If the 5th call still gives a 50x, the exception is re-raised
        and the caller should catch it
        Log messages are displayed before sleeping (when at least one exception occurred)
        """
        return self.api_client.request(*args, **kwargs)

    def add_arguments(self):
        """Override this method to add argparse argument to this worker"""

    def run(self):
        """Override this method to implement your own process"""
