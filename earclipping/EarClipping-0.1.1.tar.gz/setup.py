"""
Author:     LanHao
Date:       2020/11/10
Python:     python3.6

"""

import sys
from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="EarClipping",
    version="0.1.1",
    description="EarClipping",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bigpangl/EarClipping",
    author="LHao",
    author_email="bigpangl@163.com",
    packages=[
        "EarClipping"
    ],
    install_requires=[
        "numpy"
    ]
)
