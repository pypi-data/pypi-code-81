#!/usr/bin/env python
from os.path import join

PROJECT = "tracklr"

from tracklr import Tracklr

VERSION = Tracklr.__version__


from setuptools import setup, find_packages

try:
    long_description = open("README.rst", "rt").read()
except IOError:
    long_description = ""


def load_requirements(requirements_file):
    reqs = []
    with open(join("requirements", requirements_file)) as requirements:
        for requirement in requirements.readlines():
            if requirement.strip() and not requirement.strip().startswith("#"):
                reqs.append(requirement)
    return reqs

requirements_base = load_requirements("base.txt")
requirements_productivity = load_requirements("productivity.txt")

setup(
    name=PROJECT,
    version=VERSION,
    description="Tracklr - Command-line Productivity Toolset",
    long_description=long_description,
    author="Marek Kuziel",
    author_email="marek@kuziel.info",
    url="https://tracklr.com",
    download_url="https://gitlab.com/markuz/tracklr/-/archive/master/tracklr-master.tar.bz2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Other Audience",
        "Environment :: Console",
    ],
    platforms=["Any"],
    scripts=[],
    provides=[],
    install_requires=requirements_base,
    extras_require={
        "productivity": requirements_productivity,
    },
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["tracklr = tracklr.main:main"],
        "tracklr": [
            "group = tracklr.group:Group",
            "info = tracklr.info:Info",
            "init = tracklr.init:Init",
            "ls = tracklr.ls:Ls",
            "pdf = tracklr.pdf:Pdf",
        ],
    },
    zip_safe=False,
)
