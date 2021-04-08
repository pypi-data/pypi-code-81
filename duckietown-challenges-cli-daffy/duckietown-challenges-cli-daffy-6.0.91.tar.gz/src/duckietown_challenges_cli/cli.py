import json
import os
import sys
import traceback
from dataclasses import dataclass
from typing import Callable, Dict

import termcolor
from zuper_commons.text import format_table, indent, Style

from duckietown_challenges.col_logging import setup_logging
from duckietown_docker_utils import CONFIG_DOCKER_CREDENTIALS
from . import logger
from .cli_auth import dt_challenges_cli_auth
from .cli_build_utils import (
    dt_build_container,
    dt_check_need_upload,
    dt_check_not_dirty,
    dt_check_tagged,
    dt_dir_status,
    dt_labels,
    dt_push,
    dt_push_container,
    dt_update_reqs,
)
from .cli_common import ChallengeEnvironment
from .cli_define import dt_challenges_cli_define
from .cli_evaluate import dt_challenges_cli_evaluate
from .cli_evaluator import dt_challenges_cli_evaluator
from .cli_follow import dt_challenges_cli_follow
from .cli_info import dt_challenges_cli_info
from .cli_job import dt_challenges_cli_download
from .cli_list import dt_challenges_cli_list
from .cli_pull import dt_pull
from .cli_reset import dt_challenges_cli_reset
from .cli_retire import dt_challenges_cli_retire
from .cli_submit import dt_challenges_cli_submit
from .constants import DT1_TOKEN_CONFIG_KEY


__all__ = ["dt_challenges_cli_main", "dt_build_utils_cli_main"]


def dt_challenges_cli_main(args=None):
    description = """
    User commands
        """
    user_cmds = {
        "info": dt_challenges_cli_info,
        "evaluate": dt_challenges_cli_evaluate,
        "submit": dt_challenges_cli_submit,
        "follow": dt_challenges_cli_follow,
        "retire": dt_challenges_cli_retire,
        "list": dt_challenges_cli_list,
        "reset": dt_challenges_cli_reset,
        "evaluator": dt_challenges_cli_evaluator,
        "download": dt_challenges_cli_download,
    }
    user = CommandSection("User commands", description, user_cmds)
    admin_cmds = {
        "auth": dt_challenges_cli_auth,
        "define": dt_challenges_cli_define,
    }
    description = """
        Admin commands
            """

    admin = CommandSection(title="Admin commands", description=description, cmds=admin_cmds)
    sections = {
        "user": user,
        "admin": admin,
    }

    # noinspection PyBroadException
    try:
        dt_challenges_cli_main_(args=args, sections=sections, main_cmd="challenges")
    except SystemExit:
        raise
    except BaseException:
        logger.error(traceback.format_exc())
        sys.exit(32)


@dataclass
class CommandSection:
    title: str
    description: str
    cmds: Dict[str, Callable]


def dt_build_utils_cli_main(args=None):
    description = """
Common commands for building.
    """
    common = CommandSection(
        title="Common commands",
        description=description,
        cmds={
            "aido-container-build": dt_build_container,
            "aido-container-push": dt_push_container,
            # "bump": bump,
            "update-reqs": dt_update_reqs,
        },
    )
    exotic = CommandSection(
        title="More exotic commands",
        description=description,
        cmds={
            "dir-status": dt_dir_status,
            "check-tagged": dt_check_tagged,
            "check-not-dirty": dt_check_not_dirty,
            "check-need-upload": dt_check_need_upload,
            "labels": dt_labels,
            "push": dt_push,
        },
    )
    development = CommandSection(
        title="Commands in development",
        description=description,
        cmds={"dt-library-upload": dt_push_container, "pull": dt_pull,},
    )
    sections = {"common": common, "exotic": exotic, "development": development}
    # noinspection PyBroadException
    try:
        dt_challenges_cli_main_(args=args, sections=sections, main_cmd="devel_build")
    except SystemExit as e:
        if e.code != 0:
            logger.error(f"Exiting with {e.code}")
        raise
    except BaseException:
        logger.error(traceback.format_exc())
        sys.exit(32)


def get_commands_help_summary(sections: Dict[str, CommandSection]) -> str:
    lines = []
    for k, v in sections.items():
        lines.append(f"# {v.title}")
        lines.append(f"")
        lines.append(f"{v.description.strip()}")
        lines.append(f"")
        s = get_commands_help_summary_section(v.cmds)
        lines.append(indent(s, "   "))
        lines.append(f"")
    return "\n".join(lines)


def get_commands_help_summary_section(cmds: Dict[str, Callable]):
    cells = {}
    for i, (cmd, f) in enumerate(cmds.items()):
        cells[(i, 0)] = termcolor.colored(cmd, "green")
        doc = getattr(f, "__doc__", None)
        if doc is None:
            doc = "(description not available)"
        cells[(i, 1)] = doc

    col_style = {0: Style(halign="right")}

    return format_table(cells, style="none", col_style=col_style)


def dt_challenges_cli_main_(sections: Dict[str, CommandSection], main_cmd: str, args=None):
    setup_logging()

    if args is None:
        args = sys.argv[1:]

    if not args:
        msg = "Need to pass at least one command among the following."
        msg += "\n\n" + get_commands_help_summary(sections)
        logger.error(msg)
        sys.exit(2)

    fn = "/credentials"
    if os.path.exists(fn):

        with open(fn) as f:
            c = f.read()
        data = json.loads(c)
        credentials = data[CONFIG_DOCKER_CREDENTIALS]
        if credentials is None:
            credentials = {}
        # docker_username = data[CONFIG_DOCKER_USERNAME]
        # docker_password = data[CONFIG_DOCKER_PASSWORD]
        token = data[DT1_TOKEN_CONFIG_KEY]
        logger.debug(credentials_available=list(credentials))
    else:
        logger.warning(f"File {fn} does not exist.")
        credentials = {}
        token = None

    first = args[0]
    rest = args[1:]
    cmds = {}
    for v in sections.values():
        cmds.update(v.cmds)

    if first in cmds:
        prog = f"dts {main_cmd} {first}"
        environment = ChallengeEnvironment(token=token, docker_credentials=credentials, prog=prog,)

        f = cmds[first]
        f(rest, environment)
    else:
        msg = f"""Cannot find command "{first}". \n\n"""
        # known = indent("\n".join(sorted(cmds)), "  ")
        msg += f"I know the following commands:\n\n"
        msg += get_commands_help_summary(sections)
        logger.error(msg, args=args)
        sys.exit(3)
        # raise ZException(msg, args=args, first=first, rest=" ".join(rest))
