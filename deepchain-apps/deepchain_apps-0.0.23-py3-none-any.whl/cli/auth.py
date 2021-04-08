"""Module that allow the authentification by register the personnal token"""

import getpass
import json
from json import JSONDecodeError

from deepchainapps.utils.common import _create_config_file, _create_deechpain_folder


def login_args_configuration(sub_parser):
    """
    Login subparser that add the default login function to the parser
    """
    login_parser = sub_parser.add_parser(name="login", help="login to deepchain")
    login_parser.set_defaults(func=login)


def login(_):
    """
    Login function that create a subdirectory and store the token
    We first create .deepchain folder, then config file if not exist
    The open the file in r+ mode to not erase previous info
    """
    root_path = _create_deechpain_folder()
    path = _create_config_file(root_path)

    data = {}
    with open(path, "r+") as config_file:
        try:
            data = json.load(config_file)
        except JSONDecodeError:
            pass

        data["pat"] = getpass.getpass("PAT:")
        data["size_limit"] = 40
        config_file.seek(0)  # reset file position to the beginning.
        json.dump(data, config_file, indent=4)
        config_file.truncate()  # remove remaining part
