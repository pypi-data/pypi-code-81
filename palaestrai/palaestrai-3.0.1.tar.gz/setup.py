#!/usr/bin/env python3
"""Setup file for the ARL package."""
from setuptools import find_packages, setup


with open("VERSION") as freader:
    VERSION = freader.readline().strip()

with open("README.rst") as freader:
    README = freader.read()

install_requirements = [
    # CLI
    "click",
    "appdirs",
    # YAML
    "ruamel.yaml",
    # Process and IPC handling
    "aiomultiprocess",
    "setproctitle",
    "pyarrow",
    "zmq",
    # Data handling and storage
    "alembic",
    "numpy",
    "pandas",
    "psycopg2-binary",
    "six",
    "jsonpickle",
    "SQLalchemy < 1.4.0",
    "sqlalchemy_utils"
]

development_requirements = [
    # Tests
    "tox",
    "robot",
    "robotframework",
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "coverage",
    "mypy",
    "black",
    "lxml",
]

extras = {"dev": development_requirements}

setup(
    name="palaestrai",
    version=VERSION,
    description="A Training Ground for Autonomous Agents",
    long_description=README,
    author="The ARL Developers",
    author_email="eric.veith@offis.de",
    python_requires=">=3.8.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPLv2",
    url="http://palaestr.ai/",
    entry_points="""
        [console_scripts]
        palaestrai=palaestrai.cli.manager:cli
        arl-apply-migrations=palaestrai.store.migrations.apply:main
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
