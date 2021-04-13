#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools


with open("README.md", "r", encoding = "utf-8") as readme:
    doc = readme.read()


setuptools.setup(
    name = "throws",
    version = "1.0.2",
    description = "Python implementation of Javas @throws(...) function decorator!",
    long_description = doc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/thahnen/throws",
    author = "Tobias Hahnen",
    author_email = "hahnen.tobi@gmail.com",
    license = "MIT License",
    license_files = ["LICENSE"],
    packages = ["throws"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable"
    ],
)
