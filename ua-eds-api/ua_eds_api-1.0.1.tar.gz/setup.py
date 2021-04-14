import os
from setuptools import setup, find_packages


def readme(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as file:
        return file.read()


setup(
    name="ua_eds_api",
    version="1.0.1",
    packages=find_packages(),
    author="Ryan Johannes-Bland",
    author_email="rjjohannesbland@email.arizona.edu",
    description=(
        "Provides easy interface for making REST requests to University of "
        "Arizona EDS registry."
    ),
    long_description=readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/UACoreFacilitiesIT/UA-EDS-API",
    license="MIT",
    install_requires=["requests", "bs4"],
)
