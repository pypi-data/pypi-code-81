from string import ascii_letters
from distutils.dir_util import copy_tree
from random import choice
import os
from marshmallow import Schema
from typing import Callable, List
from zemfrog.exception import ZemfrogTemplateNotFound

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def get_template(*paths) -> str:
    """
    Function to get template base directory.

    :param paths: template directory or file name.

    :raises: ZemfrogTemplateNotFound

    """

    t = os.path.join(TEMPLATE_DIR, *paths)
    if not (os.path.isdir(t) or os.path.isfile(t)):
        raise ZemfrogTemplateNotFound("unknown template %r" % os.sep.join(paths))

    return t


def copy_template(name: str, dst: str):
    """
    Function for copying templates.

    :param name: template directory name.
    :param dst: Destination output.

    """

    t = get_template(name)
    copy_tree(t, dst)


def generate_random_string(length):
    """Make random upper / lower case depending on length.

    Args:
        length (int): letter length
    """

    rv = ""
    while len(rv) != length:
        c = choice(ascii_letters)
        rv += c
    return rv


def parse_args_to_spec(func: Callable):
    apispec = getattr(func, "_apidoc", {})
    args: List[dict] = apispec.get("arguments", {}).get("parameters", [])
    data = {}
    for a in args:
        schema = a["schema"]
        if isinstance(schema, dict):
            keys = list(schema.keys())
        elif isinstance(schema, Schema):
            keys = list(schema.fields.keys())

        loc = a.get("in", "json")
        if loc in ("json", "form", "files", "query"):
            param = data.get(loc, {})
            for k in keys:
                param[k] = None
            data[loc] = param
        else:
            raise ValueError("parameter location is unknown: %r" % loc)

    return data


def parse_paths(url: str) -> List[str]:
    """Parse paths in the url

    Args:
        url (str): url endpoint.
    """

    paths = {}
    for p in url.split("/"):
        p = p.strip()
        if p.startswith("<") and p.endswith(">"):
            path = p.strip("<>")
            if ":" in path:
                path = path.split(":", 1)[1]
            paths[path] = None
    return paths
