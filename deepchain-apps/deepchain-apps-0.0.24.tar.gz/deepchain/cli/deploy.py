"""deploy modules helps for the deployement of application on deepchain"""

import configparser

import pkg_resources

from deepchain import log
from deepchain.utils.validation import _check_app_files, _check_checkpoint_files

from ._base_cli import upload_checkpoint, upload_code
from ._utils import (
    get_app_configuration,
    get_app_info,
    get_configuration,
    update_app_status,
)


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
    path_config = pkg_resources.resource_filename("deepchain", "cli/config.ini")
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
