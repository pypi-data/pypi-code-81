#!/usr/bin/python

from setuptools import setup, find_packages
VERSION = '0.0.1'
DESCRIPTION = "Python package on numbers"
LONG_DESCRIPTION = "Python package on numbers with a slightly longer description"
setup(
    name = "Carsbypurnachandrarao",
    version = VERSION,
    author = "Purna Chandra Rao",
    author_email = "gpurna96@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords = ['Python', 'numbers'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]

)