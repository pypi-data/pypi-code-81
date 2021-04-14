"""scaffold module helps for the creation of new apps"""

import glob
import json
import os
import shutil
import tempfile
from json import JSONDecodeError
from typing import Dict

import requests
from deepchainapps import log
from deepchainapps.utils.common import _create_apps_file, _create_deechpain_folder


def save_app(app_name: str, dest_path: str) -> None:
    """
    Save complete path where the app is stored
    The app can be deploy next from any folder
    """
    root_path = _create_deechpain_folder()
    path = _create_apps_file(root_path)

    data = {}
    with open(path, "r+") as app_file:
        try:
            data = json.load(app_file)
        except JSONDecodeError:
            pass

        data[app_name] = {"dir": os.path.abspath(dest_path), "status": "local"}
        app_file.seek(0)  # reset file position to the beginning.
        json.dump(data, app_file)
        app_file.truncate()  # remove remaining part


def create_base_app(args) -> None:
    """
    Main function to:
        - download latest release
        - create tmp_directory
        - unpack folder
        - remove tmp files
    """
    log.info("download base app")
    latest_release = fetch_latest_version()
    temp_dir = tempfile.mkdtemp()
    download_latest_version(latest_release, temp_dir)
    dest_path = os.path.join(args.dir, args.app_name)
    unpack_base_repository(dest_path, latest_release, temp_dir)
    save_app(args.app_name, dest_path)
    shutil.rmtree(temp_dir)


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


def scaffold_args_configuration(sub_parser) -> None:
    """
    Configuration parser to create a folder
    """
    scaffold_parser = sub_parser.add_parser(
        name="create", help="create scaffold for new app"
    )
    scaffold_parser.add_argument(
        "app_name", action="store", help="this will be the app name in deep-chain"
    )
    scaffold_parser.add_argument(
        "--dir",
        action="store",
        default=os.curdir,
        help="the directory where the app will be created",
    )
    scaffold_parser.set_defaults(func=create_base_app)
