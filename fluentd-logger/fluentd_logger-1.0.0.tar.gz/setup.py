# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fluentd_logger",
    version="1.0.0",
    author="Catalin Dinuta",
    author_email="constantin.dinuta@gmail.com",
    description="Simple fluentd logger library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/estuaryoss/test-libs-python/tree/master/fluentd_logger",
    packages=["fluentd_logger"],
    install_requires=[
        "click",
        "fluent-logger",
        "setuptools==44.0.0",
        "jproperties"
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
