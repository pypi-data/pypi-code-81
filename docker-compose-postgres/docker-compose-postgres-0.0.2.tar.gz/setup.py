import os.path
import re
from setuptools import setup

(__version__,) = re.findall("__version__.*\s*=\s*[']([^']+)[']",
    open('docker_compose_postgres/__init__.py').read())

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="docker-compose-postgres",
    version=__version__,
    description=
    "Simplify work with postgres inside docker-compose service",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/d10xa/docker-compose-postgres",
    author="d10xa",
    author_email="d10xa@mail.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["docker_compose_postgres"],
    include_package_data=True,
    install_requires=[
        "pyyaml"
    ],
    entry_points={"console_scripts": [
        "docker-compose-postgres=docker_compose_postgres.__init__:main"]},
)
