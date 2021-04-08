from contextlib import contextmanager
from dataclasses import dataclass

import termcolor
from zuper_commons.text import indent
from zuper_commons.types import check_isinstance

from duckietown_build_utils import DockerCredentials
from duckietown_challenges import InvalidConfiguration, NotAuthorized, NotFound, ServerIsDown

__all__ = ["ChallengeEnvironment", "wrap_server_operations", "sprint"]


@dataclass
class ChallengeEnvironment:
    token: str
    docker_credentials: DockerCredentials
    prog: str

    def __post_init__(self):
        check_isinstance(self.docker_credentials, dict, _=self)


@contextmanager
def wrap_server_operations():
    try:
        yield
    except ServerIsDown as e:
        msg = "Server is down; try again later."
        msg += f"\n\n{e}"
        raise InvalidConfiguration(msg) from None

    except NotAuthorized as e:
        # msg = 'You are not authorized to perform the operation.'
        # msg += f'\n\n{e}'
        msg = str(e)
        raise InvalidConfiguration(msg) from None
    except NotFound as e:
        msg = str(e)
        raise InvalidConfiguration(msg) from None


def sprint(s: str):
    prefix = termcolor.colored("~", "yellow") + " " * 8
    s = indent(s, prefix)
    print("\n" + s + "\n")
