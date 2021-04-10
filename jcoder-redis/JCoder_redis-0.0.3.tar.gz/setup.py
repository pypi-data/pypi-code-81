#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/4/10 11:01   satan      1.0         None
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JCoder_redis",
    version="0.0.3",
    author="satan404",
    author_email="11912823@mail.sustech.edu.cn",
    description="This Redis is a Python library based on redis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satans404/repackaged_redis_for_JCoder",
    packages=setuptools.find_packages(),
    install_requires = ['redis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
