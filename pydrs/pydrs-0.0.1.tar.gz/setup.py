#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages
from pydrs import __author__, __version__
import pkg_resources


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


with open(get_abs_path("README.md"), "r") as _f:
    long_description = _f.read().strip()

with open(get_abs_path("requirements.txt"), "r") as _f:
    _requirements = _f.read().strip().split("\n")

setup(
    author=__author__,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    description="",
    download_url="https://github.com/lnls-sirius/pydrs",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="pydrs",
    url="https://github.com/lnls-sirius/pydrs",
    version=__version__,
    install_requires=_requirements,
    include_package_data=True,
    packages=find_namespace_packages(include=["pydrs", "pydrs.*"]),
    python_requires=">=3.6",
    scripts=[
        "scripts/hradc_scope.py",
        "scripts/update_hradc.py"
    ],
    zip_safe=False,
)
