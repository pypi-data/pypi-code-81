"""deploy modules helps for the deployement of application on deepchain"""

import argparse
import configparser
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

import pkg_resources
import requests
from deepchainapps import ConfigNotFoundError, log
from deepchainapps.utils.common import (
    get_app_configuration,
    get_app_info,
    update_app_status,
)
from deepchainapps.utils.validation import _check_app_files, _check_checkpoint_files


def deploy_args_configuration(sub_parser):
    """
    Main parser for deployement
    Define 'Deploy' as default function
    """
    login_parser = sub_parser.add_parser(
        name="deploy", help="deploy your app to deepchain"
    )
    login_parser.add_argument(
        "app_name",
        action="store",
        type=str,
        help="app name",
    )
    login_parser.add_argument(
        "--checkpoint",
        action="store_const",
        default=False,
        const=True,
        help="use this flag to include checkpoint during upload",
    )
    login_parser.set_defaults(func=deploy)


def deploy(args):
    """
    Deploy function:
        - Read config.ini
    upload checkpoints to deepchain
    """
    config = configparser.ConfigParser()
    path_config = pkg_resources.resource_filename("deepchainapps", "cli/config.ini")
    config.read(path_config)
    url = config["APP"]["DEEP_CHAIN_URL"]
    configuration = get_configuration()
    pat = configuration["pat"]

    app_name = args.app_name
    app_dir = get_app_info(app_name)
    status = get_app_info(app_name, kind="status")

    if status == "upload":
        msg = f"app {app_name} already uploaded, do you want to replace it? (y/n) "
        answer = input(msg)
        while answer not in ["y", "n"]:
            answer = input(msg)

        if answer == "n":
            return

    log.info("Check files before upload...")
    _check_app_files(app_name)
    score_configuration = get_app_configuration(app_name)

    req = upload_code(app_dir, args, pat, url, score_configuration)
    if req.status_code != 200:
        log.warning("api return %s stopping operation.", req.status_code)
        log.warning("App not uploaded.")
        return
    log.info("App has been uploaded.")
    update_app_status(app_name, status="upload")

    if args.checkpoint:
        _check_checkpoint_files(app_name)
        req = upload_checkpoint(app_dir, args, pat, url, configuration["size_limit"])
        if req.status_code != 200:
            log.warning("api return %s stopping operation", req.status_code)
            log.warning("Checkpoint not uploaded.")
            return

        log.info("Checkpoint has been uploaded.")

    return


def upload_code(
    app_dir: str,
    args: argparse.ArgumentParser,
    pat: str,
    url: str,
    score_configuration: List[str],
) -> None:
    """
    Function to compress and upload code to google cloud bucket
    """
    archive = shutil.make_archive(args.app_name, "tar", root_dir=app_dir + "/src")

    with open("scores.json", "w+") as config_file:
        json.dump(score_configuration, config_file)

    req = requests.post(
        url=url + args.app_name,
        headers={"authorisation": pat},
        files={
            "code": ("code.tar", open(archive, "rb"), "application/octet-stream"),
            "configuration": (
                "scores.json",
                open("scores.json", "rb"),
                "application/json",
            ),
        },
    )

    os.remove(archive)
    os.remove("scores.json")
    return req


def get_configuration() -> Dict:
    """
    Get personal access token. User must use 'login' function at least once
    Get maximal file size can be uploaded. User must use 'login' function at least once
    """
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    if not path.is_file():
        raise ConfigNotFoundError

    with open(path, "r") as config_file:
        try:
            data = json.load(config_file)
        except FileNotFoundError as err:
            raise ConfigNotFoundError from err
    return data


def upload_checkpoint(
    app_dir: str, args: argparse.ArgumentParser, pat: str, url: str, size_limit: int
) -> None:
    """
    Tar checkpoints files and upload to deepchain
    """
    signed_url = get_object_storage_url(args, pat, url)

    archive = shutil.make_archive(
        "checkpoint",
        "tar",
        app_dir + "/checkpoint",
    )
    if os.stat(archive).st_size / (1024 * 1024) > size_limit:
        print(f"Can not upload files over {size_limit}MB")
    else:
        req = requests.put(
            signed_url,
            data=open(archive, "rb").read(),
            headers={"Content-Type": "application/octet-stream"},
        )
    os.remove(archive)
    return req


def get_object_storage_url(args, pat: str, url: str) -> Dict:
    """
    Get the signed url to upload safely
    """
    req = requests.post(
        url=url + args.app_name + "/checkpointUrl", headers={"authorisation": pat}
    )
    signed_url = req.json()
    return signed_url
