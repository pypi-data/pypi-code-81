#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

PROJECT = "flowfusic-cli"
VERSION = "0.1.1"

# Package root directory
root_dir = Path(__file__).parent

# The text of the README file
long_description = (root_dir / "README.md").read_text()

setup(
    name=PROJECT,
    version=VERSION,
    description="Command line tool for Flowfusic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Flowfusic sp. z o.o.",
    author_email="support@flowfusic.com",
    url="https://github.com/flowfusic/flowfusic-cli",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    keywords="flowfusic",
    install_requires=[
        "click==7.1.2",
        "clint==0.5.1",
        "halo==0.0.31",
        "requests==2.25.1",
        "requests-toolbelt==0.9.1",
        "marshmallow==3.0.0a1",
        "pytz>=2016.10",
        "tabulate==0.8.7",
        "pathlib2==2.3.5",
        "PyYAML",
        "raven",
        "scandir;python_version<'3.5'",
    ],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "flowfusic = src.main:cli",
            "flowfusic-dev = src.development.dev:cli"
        ],
    },
    tests_require=[
        "pytest",
        "mock>=1.0.1",
    ],
)
