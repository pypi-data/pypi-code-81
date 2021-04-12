#!/usr/bin/env python

# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

import io
import os
import sys

from shutil import rmtree

from setuptools import find_packages, setup, Command


# Package metadata
NAME = "couplet-composer"
DESCRIPTION = "Tool for building, testing, and preparing binary " \
    "distribution archives of Obliging Ode and Unsung Anthem."
URL = "https://github.com/anttikivi/couplet-composer"
EMAIL = "antti.kivi@visiosto.fi"
AUTHOR = "Antti Kivi"
REQUIRES_PYTHON = ">=2.7.11"
VERSION = None

# The packages that Couplet Composer needs
with open("requirements.txt") as f:
    REQUIRED = f.read().splitlines()

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in the MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the __version__.py module of the package as a dictionary.
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable
        ))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": ["couplet-composer = couplet_composer.__main__:run"]
    },
    install_requires=REQUIRED,
    package_data={"": ["*.json"]},  # TODO This might be unnecessary
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ],
    cmdclass={
        "upload": UploadCommand,
    }
)
