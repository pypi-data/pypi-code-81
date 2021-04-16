#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "cpmsy",
    version = "0.1.3",
    author = "yangmiao",
    author_email = "1446174581@qq.com",
    description = "point cloud match",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    url = "https://pypi.org/manage/projects/cpmsy",
    packages = ['cpmsy'],
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)