#!/usr/bin/env python
# encoding: UTF-8

import ast
from setuptools import setup
import os.path

__doc__ = open(
    os.path.join(os.path.dirname(__file__), "README.rst"),
    "r"
).read()

try:
    # For setup.py install
    from tos import __version__ as version
except ImportError:
    # For pip installations
    version = str(ast.literal_eval(
        open(os.path.join(
            os.path.dirname(__file__),
            "tos",
            "__init__.py"),
            "r"
        ).read().split("=")[-1].strip()
    ))

setup(
    name="theatre_of_spud",
    version=version,
    description="A text-driven web game.",
    author="D E Haynes",
    author_email="tundish@gigeconomy.org.uk",
    url="https://github.com/tundish/theatre_of_spud",
    long_description=__doc__,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Affero General Public License v3"
        " or later (AGPLv3+)"
    ],
    packages=[
        "tos", "tos.test",
        "tos.dlg.act01",
        "tos.dlg.act03",
        "tos.mixins", "tos.mixins.test",
        "tos.web",
    ],
    package_data={
        "tos.dlg.act01": ["*.rst"],
        "tos.dlg.act03": ["*.rst"],
        "tos.web": [
            "css/*.css",
            "*.html",
        ],
    },
    install_requires=[
        "aiohttp>=3.7.3",
        "turberfield-catchphrase>=0.18.0",
    ],
    extras_require={
        "dev": [
            "flake8>=3.9.0",
            "wheel>=0.36.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "tos-cli = tos.main:run",
        ],
    },
    zip_safe=True,
)
