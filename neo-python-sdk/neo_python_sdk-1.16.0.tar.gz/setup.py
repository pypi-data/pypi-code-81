from setuptools import setup
from distutils.core import setup
import os

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

__sdk_version__ = os.getenv("SDK_VERSION")

with open(os.path.join(this_directory, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="neo_python_sdk",
    packages=["neo_python_sdk"],
    version=__sdk_version__,
    python_requires=">=3.5",
    license="apache-2.0",
    description="Neo SDK for Python with some additional libraries to support the development of Neo Sentinels (NSX).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jan-Eric Gaidusch <Neohelden GmbH>",
    url="https://github.com/neohelden/neo_python_sdk",
    keywords=["neohelden", "neo", "neo-sdk"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
