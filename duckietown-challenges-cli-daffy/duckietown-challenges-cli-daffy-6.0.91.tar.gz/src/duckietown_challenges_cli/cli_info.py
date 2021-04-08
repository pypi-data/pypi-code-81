import argparse
from typing import List

import termcolor

from duckietown_challenges import get_dtserver_user_info, get_duckietown_server_url
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations

__all__ = ["dt_challenges_cli_info"]


def dt_challenges_cli_info(args: List[str], environment: ChallengeEnvironment):
    """ Information about your account. """
    parser = argparse.ArgumentParser(prog=environment.prog)
    parser.add_argument("--impersonate", type=str, default=None)

    parsed = parser.parse_args(args)

    token = environment.token

    with wrap_server_operations():
        info = get_dtserver_user_info(token, impersonate=parsed.impersonate)

        NOT_PROVIDED = termcolor.colored("missing", "red")

        if "profile" in info:
            profile = href(info.get("profile"))
        else:
            profile = NOT_PROVIDED

        user_login = info.get("user_login", NOT_PROVIDED)
        display_name = info.get("name", NOT_PROVIDED)
        uid = info.get("uid", NOT_PROVIDED)

        s = """

    You are succesfully authenticated:

             ID: {uid}
           name: {display_name}
          login: {user_login}
        profile: {profile}

    """.format(
            uid=bold(uid), user_login=bold(user_login), display_name=bold(display_name), profile=profile,
        ).strip()

        server = get_duckietown_server_url()

        url = server + "/humans/users/%s" % info["uid"]

        s += """

    You can find the list of your submissions at the page:

        {url}

            """.format(
            url=href(url)
        )

        sprint(s)
        #
        # ri = get_registry_info(token)
        # shell.ssprint('Registry: %s' % ri.registry)

        # sprint(' github: %s' % (info['github_username'] or NOT_PROVIDED))


def href(x):
    return termcolor.colored(x, "blue", attrs=["underline"])


def bold(x):
    return termcolor.colored(x, attrs=["bold"])
