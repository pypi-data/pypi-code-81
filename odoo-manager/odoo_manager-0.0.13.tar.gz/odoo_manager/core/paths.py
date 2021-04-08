import os
from glob import glob
from odoo_manager.cli.exceptions import CommandException

pipe_dev_null = "> /dev/null 2>&1"

# This is the file pattern which indicates the project root directory.
COMPOSE_PATTERN = "docker-compose.*yml"


class Paths(object):
    base_path = None

    def __init__(self):
        """
        Initialize a Paths object.
        """
        iterated = 0
        working_dir = os.getcwd()

        while not self.base_path and iterated < 100:
            iterated += 1
            compose_filenames = glob(COMPOSE_PATTERN)
            for compose_filename in compose_filenames:
                if os.path.isfile(os.path.join(working_dir, compose_filename)):
                    self.base_path = working_dir
                    break
            working_dir = os.path.abspath(os.path.join(working_dir, ".."))

        if not self.base_path:
            raise CommandException(
                "We cannot find a valid project. Make sure that you are inside of an Odoo project with a docker-compose.yml file."
            )

    def base(self, path=""):
        """
        Helper method to ensure all paths are relative to tasks.py.

        :param path:
        :return:
        """
        return os.path.join(self.base_path, path)


def iterate_py_files(fn, base):
    """
    :param fn:
    :return {NoneType}:
    """
    ignore = [".container", ".deployment", ".docs", ".githooks", ".monitoring", ".om", "_lib", "_lib_static"]
    for dirpath, dirs, filenames in os.walk(base, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore]
        for filename in [f for f in filenames if f.endswith(".py") and f not in ignore]:
            fn(filename, os.path.join(dirpath, filename))


def iterate_odoo_modules(fn):
    """
    :param fn:
    :return {NoneType}:
    """
    pass
