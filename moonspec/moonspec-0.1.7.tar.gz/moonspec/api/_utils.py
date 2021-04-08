import grp
import importlib
import pwd

# NOTE: these are internal methods and you should not be using them -
#       they CAN and WILL be replaced, and are not part of the public API!
from typing import List, Optional


def _get_pwd_user_by_name(name: str) -> Optional[pwd.struct_passwd]:
    # noinspection PyBroadException
    try:
        return pwd.getpwnam(name)
    except:
        return None


def _get_pwd_group_by_name(name: str) -> Optional[grp.struct_group]:
    # noinspection PyBroadException
    try:
        return grp.getgrnam(name)
    except:
        return None


def _get_pwd_users() -> List[pwd.struct_passwd]:
    # noinspection PyBroadException
    try:
        return pwd.getpwall()
    except:
        return []


def _get_pwd_groups() -> List[grp.struct_group]:
    # noinspection PyBroadException
    try:
        return grp.getgrall()
    except:
        return []


def _has_python_library(name: str) -> bool:
    if not hasattr(importlib, 'util'):
        return importlib.find_loader(name) is not None
    else:
        return importlib.util.find_spec(name) is not None
