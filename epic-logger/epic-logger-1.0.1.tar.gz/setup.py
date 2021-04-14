# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Author:       ZERONE40
# Date:         2021-04-14 18:19
# Description:  

# -------------------------------------------------------------------------------

import setuptools

with open("README.MD", "r", encoding="utf-8") as read_me:
    long_description = read_me.read()

setuptools.setup(
    name="epic-logger",
    version="1.0.1",
    author="ZERONE40",
    author_email="zerone40@163.com",
    description="Write logs of multi-module programs to different files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zerone40",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
