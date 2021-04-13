"""
  _____           _     _______             _ 
 |  __ \         | |   |__   __|           | |  
 | |__) | __ ___ | |_ ___ | | ___  _ __ ___| |__
 |  ___/ '__/ _ \| __/ _ \| |/ _ \| '__/ __| '_ \ 
 | |   | | | (_) | || (_) | | (_) | | | (__| | | |
 |_|   |_|  \___/ \__\___/|_|\___/|_|  \___|_| |_|Plugin

ProtoTorch Qu Plugin Package
"""

from pkg_resources import safe_name
from setuptools import setup
from setuptools import find_packages

import ast
import importlib.util

PKG_DIR = "prototorch_qu"


def find_version():
    """Return value of __version__.

    Reference: https://stackoverflow.com/a/42269185/
    """
    file_path = importlib.util.find_spec(PKG_DIR).origin
    with open(file_path) as file_obj:
        root_node = ast.parse(file_obj.read())
    for node in ast.walk(root_node):
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and node.targets[0].id == "__version__":
                return node.value.s
    raise RuntimeError("Unable to find version string.")


VERSION = find_version()

PROJECT_URL = "https://github.com/si-cim/prototorch_qu"
DOWNLOAD_URL = "https://github.com/si-cim/prototorch_qu.git"

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ["prototorch"]

setup(
    name=safe_name(PKG_DIR),
    version=VERSION,
    descripion="Quantum Computing plugin for ProtoTorch.",
    long_description=long_description,
    author="Alexander Engelsberger",
    author_email="engelsbe@hs-mittweida.de",
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    license="MIT",
    install_requires=INSTALL_REQUIRES,
    extras_require={},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"prototorch.plugins": "qu = prototorch_qu"},
    packages=find_packages(),
    zip_safe=False,
)
