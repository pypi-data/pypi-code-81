#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="pj-scraper",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "src/pj_scraper/_version.py",
        "fallback_version": "0.0.0",
    },
    license="MIT",
    description="none",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Mattias Hornum",
    author_email="mattiashornum@gmail.com",
    url="https://github.com/mdhor/pj-scraper",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://github.com/mdhor/pj-scraper/blob/master/CHANGELOG.rst",
        "Issue Tracker": "https://github.com/mdhor/pj-scraper/issues",
    },
    keywords=[],
    python_requires=">=3.6",
    install_requires=["pandas", "beautifulsoup4", "requests", "openpyxl"],
    extras_require={},
    setup_requires=[
        "setuptools_scm",
    ],
    entry_points={
        "console_scripts": [
            "pj-scraper = pj_scraper.cli:main",
        ]
    },
)
