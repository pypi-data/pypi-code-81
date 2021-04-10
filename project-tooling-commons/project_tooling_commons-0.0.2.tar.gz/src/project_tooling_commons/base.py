"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = project_tooling_commons.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
import sys
import base64
import unicodedata
import typer

from .logger import init_logging

from project_tooling_commons import __version__

__author__ = "Juan David"
__copyright__ = "Juan David"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

app = typer.Typer()

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from project_tooling_commons.skeleton import fib`,
# when using this Python module as a library.

@app.command()
def isBase64(input_string: str):
    """Checks if a string is base64 coded

    Args:
        s (str): Input string

    Returns:
        bool: True for base64 false if not
    """
    try:
        return base64.b64encode(base64.b64decode(input_string)) == input_string
    except Exception:
        return False

@app.command()
def stripAccents(input_string: str):
    """Transforms a string switching accent characters with equivalent non accented

    Args:
        s (str): Input string

    Returns:
        str: String without accents
    """
    return ''.join(c for c in unicodedata.normalize('NFD', input_string)
                   if unicodedata.category(c) != 'Mn')        


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m project_tooling_commons.skeleton 42
    #

    init_logging()
    app()
