#!/usr/bin/env python

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    l.split("==")[0]
    for l in pathlib.Path("requirements.txt").read_text().splitlines()
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Goncalo Magno",
    author_email="goncalo@gmagno.dev",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="A simple lib for downloading nfe's",
    entry_points={"console_scripts": ["nfe_parser=nfe_parser.cli:main",],},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="nfe_parser",
    name="nfe_parser",
    packages=find_packages(include=["nfe_parser", "nfe_parser.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/gmagno/nfe_parser",
    version="0.6.1",
    zip_safe=False,
)
