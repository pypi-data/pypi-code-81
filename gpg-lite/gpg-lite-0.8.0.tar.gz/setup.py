#!/usr/bin/env python3

from datetime import datetime
from setuptools import setup, find_packages

# 0.0.0-dev.* version identifiers for development only (not public)
__version__ = "0.0.0.dev" + datetime.now().strftime("%Y%m%d")

setup(
    name="gpg-lite",
    version="0.8.0",
    license="LGPL3",
    description="python gpg bindings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jaroslaw Surkont, "
    "Gerhard Bräunlich, "
    "Robin Engler, "
    "Christian Ribeaud, "
    "François Martin",
    author_email="jaroslaw.surkont@unibas.ch, "
    "gerhard.braeunlich@id.ethz.ch, "
    "robin.engler@sib.swiss, "
    "christian.ribeaud@karakun.com, "
    "francois.martin@karakun.com",
    url="https://gitlab.com/biomedit/gpg-lite",
    python_requires=">=3.6",
    install_requires=["dataclasses ; python_version<'3.7'"],
    packages=find_packages(
        exclude=["test", "test.*", "integration_test", "integration_test.*"]
    ),
    package_data={"gpg_lite": ["py.typed"]},
    zip_safe=False,
    test_suite="test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
