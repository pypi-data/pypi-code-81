# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="excel_generator",
    version="1.0.2",
    author="Catalin Dinuta",
    license="Apache",
    author_email="constantin.dinuta@gmail.com",
    description="An excel generator that takes as input a JSON file. "
                "The format of the file is list of dictionaries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/estuaryoss/test-libs-python/tree/master/excel_generator",
    packages=["excel_generator"],
    install_requires=[
        "click",
        "pyexcel",
        "pyexcel-xls",
        "pyexcel-xlsx",
        "pyexcel-xlsxw",
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
