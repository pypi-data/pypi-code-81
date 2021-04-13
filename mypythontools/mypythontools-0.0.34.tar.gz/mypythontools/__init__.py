"""

.. image:: https://img.shields.io/pypi/pyversions/mypythontools.svg
    :target: https://pypi.python.org/pypi/mypythontools/
    :alt: Python versions

.. image:: https://badge.fury.io/py/mypythontools.svg
    :target: https://badge.fury.io/py/mypythontools
    :alt: PyPI version

.. image:: https://img.shields.io/lgtm/grade/python/github/Malachov/mypythontools.svg
    :target: https://lgtm.com/projects/g/Malachov/mypythontools/context:python
    :alt: Language grade: Python

.. image:: https://readthedocs.org/projects/mypythontools/badge/?version=latest
    :target: https://mypythontools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT


Some tools/functions/snippets used across projects.

Usually used from IDE. Used paths are infered and things like building the
application with pyinstaller, incrementing version, generating rst files for sphinx docs,
pushing to github or deploying to Pypi is matter of calling one function
or clicking one button (e.g. Vs code task).

Many projects - one codebase.

If you are not sure whether structure of your app will work with this code, there is python starter repo
on https://github.com/Malachov/my-python-starter

Paths are infered, but if you have atypical structure or have more projects in cwd, use `mypythontools.misc.set_paths()`.

Links
=====

Official documentation - https://mypythontools.readthedocs.io/
Official repo - https://github.com/Malachov/mypythontools

Installation
============

Python >=3.6 (Python 2 is not supported).

Install just with::

    pip install mypythontools

"""

from . import utils
from . import build
from . import deploy
from . import misc
from . import pyvueeel

__version__ = "0.0.34"

__author__ = "Daniel Malachov"
__license__ = "MIT"
__email__ = "malachovd@seznam.cz"

__all__ = ["utils", "build", "deploy", "misc", "pyvueeel"]
