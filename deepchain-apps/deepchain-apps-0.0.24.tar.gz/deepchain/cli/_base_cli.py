"""Main functions used in CLI"""

import argparse
import glob
import json
import os
import shutil
from typing import Dict, List

import requests
import yaml

from deepchain import log

from ._utils import _create_apps_file, _create_deechpain_folder


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


def save_app(app_name: str, dest_path: str) -> None:
    """
    Save complete path where the app is stored
    The app can be deploy next from any folder
    """
    root_path = _create_deechpain_folder()
    path = _create_apps_file(root_path)

    with open(path, "r+") as app_file:
        data = yaml.load(app_file, Loader=yaml.SafeLoader)
        data = {} if data is None else data

    data[app_name] = {"dir": os.path.abspath(dest_path), "status": "local"}
    with open(path, "w") as app_file:
        yaml.dump(data, app_file, Dumper=yaml.SafeDumper)


def fetch_latest_version() -> Dict:
    """
    Fetch info on last release version of the github repository.
    """
    url = "https://api.github.com/repos/instadeepai/deep-chain-apps/releases"
    req = requests.get(url)
    releases = req.json()
    latest_release = sorted(releases, key=lambda k: k["published_at"], reverse=True)[0]
    return latest_release


def download_latest_version(latest_release: Dict, temp_dir: str) -> None:
    """
    Function do downlad latest tarball image on github where templates are stored.
    repo link : https://github.com/instadeepai/deep-chain-apps
    """
    log.info("downloading release  from : %s", latest_release["tarball_url"])
    req = requests.get(latest_release["tarball_url"])
    with open(f"{temp_dir}/{latest_release['tag_name']}.tar", "wb") as file:
        file.write(req.content)


def unpack_base_repository(dest_path, latest_release: Dict, temp_dir: str) -> None:
    """
    Function to unpack the github tar image download.
    Data are copied in a tmp folder
    """
    shutil.unpack_archive(
        f"{temp_dir}/{latest_release['tag_name']}.tar",
        f"{temp_dir}/{latest_release['tag_name']}",
    )
    for file in glob.glob(
        rf"{temp_dir}/{latest_release['tag_name']}/*/**", recursive=True
    ):
        shutil.copytree(file, dest_path)
        break
