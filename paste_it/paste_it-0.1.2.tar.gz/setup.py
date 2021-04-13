#!/usr/bin/env python3
from setuptools import setup # type: ignore

def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="paste_it",
    version="0.1",
    description="a cli script and tiny library to upload files to pastebin",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/advaithm/paste_it",
    author="nullrequest",
    author_email="advaith.madhukar@gmail.com",
    license="GPLv3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["paste_it"],
    include_package_data=True,
    install_requires=["requests", "rich"],
    entry_points={"console_scripts": ["paste_it=paste_it.command_line:main"]},
    zip_safe=False,
)
