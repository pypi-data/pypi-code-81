import requests
from requests.exceptions import HTTPError
import json
import os
import base64
import sys
from enum import Enum
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")


class OS(Enum):

    WINDOWS = 1
    LINUX = 2
    MAC = 3


API_VERSION = "2.0"
host = os.environ["DATABRICKS_API_HOST"]
token = os.environ["DBUTILSTOKEN"]


def api_get(api: str, function: str, data: dict = None, query: str = None):

    url = f"{host}/api/{API_VERSION}/{api}/{function}"
    if query:
        url = f"{url}?{query}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url=url, headers=headers, json=data)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        logger.error(msg)
        raise e

    return response.json()


def api_post(api: str, function: str, data: dict):

    url = f"{host}/api/{API_VERSION}/{api}/{function}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url=url, headers=headers, json=data)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        logger.error(msg)
        raise e

    return response.json()


def base64_decode(base64_string: str, encoding: str = "utf-8"):

    base64_bytes = base64_string.encode(encoding)
    content_bytes = base64.b64decode(base64_bytes)

    return content_bytes


def base64_encode(string_bytes: bytes, ecoding: str = "utf-8"):

    base64_bytes = base64.b64encode(string_bytes)

    return base64_bytes.decode(ecoding)


def is_windows():

    return sys.platform in ["win32", "cygwin", "msys"]


def format_path_for(path: str, os: OS):

    if os in (OS.LINUX, OS.MAC):
        return path.replace("\\", "/")

    elif os == OS.WINDOWS:
        return path.replace("/", "\\")


def format_path_for_os(path: str):

    if sys.platform in ["win32", "cygwin", "msys"]:
        return format_path_for(path, OS.WINDOWS)

    elif sys.platform in ["linux", "linux2"]:
        return format_path_for(path, OS.LINUX)

    elif sys.platform in ["darwin"]:
        return format_path_for(path, OS.MAC)

    else:
        raise Exception(
            f"Error formating path={path} for os. Operating system not supported {sys.platform}"
        )
