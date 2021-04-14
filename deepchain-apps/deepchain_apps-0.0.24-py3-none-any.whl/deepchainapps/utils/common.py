"""Common functions for CLI module"""

import importlib
import json
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List

from .exceptions import AppNotFoundError, AppsNotFoundError


def get_app_info(app_name: str, kind: str = "dir") -> str:
    """
    Get the directory of the application save in the deepchain config file
    """
    assert kind in ["dir", "status"], "Can on only select 'dir' or 'status'"

    config = get_apps_config()
    app_info = config.get(app_name, None)

    if app_info is None:
        raise AppNotFoundError(app_name)

    return app_info[kind]


def get_apps_config() -> Dict:
    """
    Get app config files
    """
    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    if not path.is_file():
        raise AppsNotFoundError

    data = {}
    with open(path, "r") as apps_file:
        try:
            data = json.load(apps_file)
        except (FileNotFoundError, JSONDecodeError):
            pass

    return data


def get_app_configuration(app_name: str) -> List[str]:
    """
    Function to get the score_names of the app and regitrer it
    This function requires to load the module and get the app
    names via a @staticmethod
    """
    app_dir = get_app_info(app_name)
    app_dir = Path(app_dir)

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".src.app")
    scores = mod.App.score_names()
    # Remove last element of the path which was added manually
    sys.path.pop(-1)

    return scores


def _create_deechpain_folder() -> Path:
    """create .deepchain folder if not exist"""
    path = Path.home().joinpath(".deep-chain")
    path.mkdir(exist_ok=True)
    return path


def _create_config_file(root_path: Path) -> Path:
    """
    create the config file to store the personal access token
    """
    path = root_path.joinpath("config")
    path.touch(exist_ok=True)
    return path


def _create_apps_file(root_path: Path) -> Path:
    """
    create the apps file to store all the apps
    """
    path = root_path.joinpath("apps")
    path.touch(exist_ok=True)
    return path


def update_app_status(app_name: str, status: str = "upload") -> None:
    """update the status of the app"""

    path = Path.home().joinpath(".deep-chain").joinpath("apps")

    data = {}
    with open(path, "r+") as app_file:
        try:
            data = json.load(app_file)
        except JSONDecodeError:
            pass

        data[app_name]["status"] = status
        app_file.seek(0)  # reset file position to the beginning.
        json.dump(data, app_file)
        app_file.truncate()  # remove remaining part
