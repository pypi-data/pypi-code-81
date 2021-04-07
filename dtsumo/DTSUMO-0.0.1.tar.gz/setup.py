# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:21:10 2021

@author: HUGUO
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DTSUMO",
    version="0.0.1",
    author="Example Author",
    author_email="weikeguojing@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wkgj",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)