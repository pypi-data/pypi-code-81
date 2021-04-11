"""Store and retrieve credentials and configuration

Handle serialization, deserialization and encryption for password.
"""

import getpass
import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable

import requests
import urllib3
from cryptography.fernet import Fernet
from toolz import pipe
from urllib3.exceptions import InsecureRequestWarning
from loguru import logger


@dataclass
class Config:
    knox_url: str
    user: str
    password: str


@lru_cache(None)
def get_config(
    persistent_path: Path,
    key: str,
    knox_url: str,
    validate_credential: Callable = lambda user, password: True,
) -> Config:

    if not persistent_path.is_file():
        logger.info("no configuration found")
        configure(
            key,
            validate_credential,
            persistent_path,
            prompt={"user": "user", "password": "password"},
        )
    creds = json.loads(persistent_path.read_text())
    return Config(knox_url=knox_url, **creds)


def configure(key: str, validate_credential: Callable, persistent_path: Path, prompt):
    """Iteractive user/password inputs

    First, try to retrieve user/password from ENV (`user`,`password`)
    fallback on asking them.

    You can customize labels for interaction using  `prompt`
    with a dict following this structure : {"user": "Your Username", "password": "Your Password"}
    """
    try:
        user = os.environ["user"]
        password = os.environ["password"]
        logger.info("use ENV for credentials")
    except KeyError:
        logger.info("Interactive configuration")
        user = input(prompt["user"])
        password = getpass.getpass(prompt["password"])
    if validate_credential(user, password):
        logger.info(f"Credential verification OK for user {user}")
        persistent_path.write_text(
            json.dumps({"user": user, "password": encrypt(key, password)})
        )
        logger.info("Configuration saved")
    else:
        logger.info("Not able to connect using credentials")


def _tostr(data: bytes) -> str:
    return data.decode("utf8")


def _tobytes(data: str) -> bytes:
    return bytes(data, "utf8")


def encrypt(key: str, password: str) -> str:
    f = Fernet(_tobytes(key))
    return pipe(password, _tobytes, f.encrypt, _tostr)


def decrypt(key: str, encrypted: str) -> str:
    f = Fernet(_tobytes(key))
    return pipe(encrypted, _tobytes, f.decrypt, _tostr)


def validate(key: str, conf: Config) -> bool:
    """ping knox url with credentials in `conf`"""

    urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(conf.knox_url, auth=(conf.user, decrypt(key, conf.password)))
    return r.status_code == 200
