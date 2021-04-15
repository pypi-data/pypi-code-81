"""Aliyun Encryption SDK for Django."""
import os
import re

from setuptools import find_packages, setup

VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*args):
    """Reads complete file contents."""
    return open(os.path.join(HERE, *args)).read()


def get_version():
    """Reads the version from this module."""
    init = read("src", "constants.py")
    return VERSION_RE.search(init).group(1)


def get_requirements():
    """Reads the requirements file."""
    requirements = read("requirements.txt")
    return list(requirements.strip().splitlines())


setup(
    name="django-encryption-sdk",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url='https://github.com/vlean/django-encryption-sdk',
    version=get_version(),
    author="vlean",
    author_email='vlean@qq.com',
    maintainer="vlean",
    description="Encryption SDK implementation for Django",
    long_description=read("README.md"),
    keywords=["django-encryption", "django-kms"],
    install_requires=get_requirements(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ],
)
