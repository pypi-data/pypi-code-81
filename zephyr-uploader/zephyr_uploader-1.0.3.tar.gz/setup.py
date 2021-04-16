# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zephyr_uploader",
    version="1.0.3",
    author="Catalin Dinuta",
    author_email="constantin.dinuta@gmail.com",
    description="Upload test execution results to Jira Zephyr. The input is an Excel document.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/estuaryoss/test-libs-python/tree/master/zephyr_uploader",
    packages=["zephyr_uploader"],
    install_requires=[
        "click",
        "pyexcel",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
