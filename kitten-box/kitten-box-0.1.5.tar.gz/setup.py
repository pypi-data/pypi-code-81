# -*- coding: utf-8 -*-
"""
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup
from setuptools.command.install import install
from kitten_box.version import VERSION


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="kitten-box",
    version=VERSION,
    description="Simple Py package",
    long_description=readme(),
    url="https://github.com/levlaz/circleci.py",
    author="mont Pasit Nusso",
    author_email="montionugera@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='sample',
    packages=['kitten_box'],
    install_requires=[
        # 'requests',
    ],
    python_requires='>=3.8',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
