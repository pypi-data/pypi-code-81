"""Setup script for pydocgen"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="pydocgen",
    version="0.0.3b",
    description="Automatically generate docstrings and documentation files for your code!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/m0bi5/pydocgen",
    author="m0bi5",
    author_email="",
    license="MIT",
    classifiers=[
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["pydocgen"],
    include_package_data=True,
    install_requires=[
        "pdoc3", "Jinja2"
    ],
    entry_points={"console_scripts": ["pydocgen=pydocgen.__main__:main"]},
)