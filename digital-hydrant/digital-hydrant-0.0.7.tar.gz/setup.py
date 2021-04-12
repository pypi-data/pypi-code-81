#!/usr/bin/env python
# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

from setuptools import setup, find_packages

version = {}
with open("digital_hydrant/__version__.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digital-hydrant",
    version=version["version"],
    author="Outside Open",
    author_email="developers@outsideopen.com",
    packages=find_packages(),
    scripts=["bin/hydrant"],
    url="https://github.com/outsideopen/digital-hydrant-collectors",
    license="GPL",
    description="Digital Hydrant Collectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "colorlog",
        "netifaces",
        "requests",
        "speedtest-cli",
        "schedule",
        "configupdater",
        "python-nmap",
    ],
    package_data={"digital_hydrant": ["config/*", "config/hydra/*", "migrations/*"]},
    platforms=["linux"],
)
