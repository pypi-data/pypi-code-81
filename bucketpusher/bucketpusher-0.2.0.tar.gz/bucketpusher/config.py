import os
import sys
import pathlib
from appdirs import AppDirs
from typing import Optional

# Path stuff
bundle_dir = pathlib.Path(getattr(sys, "_MEIPASS", "."))
client_secrets_path = bundle_dir / "data/client_secrets.pickle"
service_account_path = bundle_dir / "data/service_account.pickle"


def get_icon_path() -> Optional[pathlib.Path]:
    if os.name == "nt":
        icon_path = bundle_dir / "data/icon.ico"
    else:
        icon_path = bundle_dir / "data/icon.icns"
    if icon_path.is_file():
        return icon_path.absolute()
    return None


dirs = AppDirs("bucketpusher")
user_data_dir = pathlib.Path(dirs.user_data_dir)


def get_user_credentials_path() -> pathlib.Path:
    user_credentials_path = user_data_dir / "user_credentials.pickle"
    if not user_credentials_path.parent.is_dir():
        user_data_dir.parent.mkdir(parents=True, exist_ok=True)
    return user_credentials_path


def get_log_file_path() -> pathlib.Path:
    log_file = pathlib.Path(dirs.user_log_dir) / "bucketpusher.log"

    if not log_file.parent.is_dir():
        log_file.parent.mkdir(parents=True, exist_ok=True)
    return log_file
