"""Implementation of several functions to validate the folder to upload"""

import importlib
import os
import sys
from pathlib import Path
from typing import List

from deepchainapps import AppNotFoundError, CheckpointNotFoundError
from deepchainapps.utils.common import get_app_info


def _check_checkpoint_files(app_name: str):
    """
    Check if some files are present if the checkpoint folder
    """
    extension_list = [
        ".h5",
        ".hdf5",
        ".yaml",
        ".yml",
        ".pt",
        ".pb",
        ".pkl",
        ".ckpt",
        ".pickle",
    ]
    app_dir = Path(get_app_info(app_name))
    checkpoint_dir = app_dir.joinpath("checkpoint")
    if not checkpoint_dir.is_dir():
        raise FileNotFoundError(
            f"You must have a checkpoint folder in the {app_dir} folder"
        )

    model_found = _check_file_extension(checkpoint_dir, extension_list)
    if not model_found:
        raise CheckpointNotFoundError(extension_list)


def _check_file_extension(folder_path: Path, extension_list: List) -> bool:
    """Check if file of extension list are found in folder"""
    model_found = False
    for file in folder_path.glob("*"):
        base_file = os.path.basename(file)
        _, ext_ = os.path.splitext(base_file)

        if ext_ in extension_list:
            model_found = True
            break
    return model_found


def _check_app_files(app_name: str):
    """
    Check if the name of the app has not been modified to be upload
    on the plateform
    """
    app_dir = Path(get_app_info(app_name))

    if not app_dir.is_dir():
        raise AppNotFoundError(app_name)

    if not app_dir.joinpath("src").is_dir():
        raise NotADirectoryError("The main folder you should named 'src'")

    _check_init(app_dir)
    _check_init(app_dir.joinpath("src"))
    _check_app(app_dir.joinpath("src"))
    _check_module(app_dir, app_name)

    return


def _check_init(app_dir: Path) -> None:
    """Check if init file is in folder"""
    path_init = app_dir.joinpath("__init__.py")
    if not path_init.is_file():
        raise FileNotFoundError(
            "The app folder must be a module and contain __init__.py file"
        )


def _check_app(app_dir: Path) -> None:
    """Check if app file if in the app folder"""
    path_scorer = app_dir.joinpath("app.py")
    if not path_scorer.is_file():
        similar_file = _find_similar_file(app_dir, "app")
        message = "The app filename must be app.py"
        if similar_file is not None:
            message += f", found this similar file instead : {similar_file}"

        raise FileNotFoundError(message)


def _check_module(app_dir: Path, app_name: str) -> None:
    """Check if app module contains App class"""
    # append current path to the pkg to find the app
    # as a module

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".src.app")
    avail_members = dir(mod)
    sys.path.pop(-1)

    if "App" not in avail_members:
        raise ModuleNotFoundError("You must have a App class in your app.py module")


def _find_similar_file(path_folder: Path, pattern: str) -> str:
    """
    Find python files containing pattern in a specific folder
    """
    for file in path_folder.iterdir():
        filename = file.name
        if (filename.__contains__(pattern)) and (filename.endswith("py")):
            return filename

    return None
