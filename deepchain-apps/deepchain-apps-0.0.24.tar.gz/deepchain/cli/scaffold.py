"""scaffold module helps for the creation of new apps"""

import os
import shutil
import tempfile

from deepchain import log

from ._base_cli import (
    download_latest_version,
    fetch_latest_version,
    save_app,
    unpack_base_repository,
)


def create_base_app(args) -> None:
    """
    Main function to:
        - download latest release
        - create tmp_directory
        - unpack folder
        - remove tmp files
    """
    log.info("Download base app.")
    latest_release = fetch_latest_version()
    temp_dir = tempfile.mkdtemp()
    download_latest_version(latest_release, temp_dir)
    dest_path = os.path.join(args.dir, args.app_name)
    unpack_base_repository(dest_path, latest_release, temp_dir)
    save_app(args.app_name, dest_path)
    shutil.rmtree(temp_dir)


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
