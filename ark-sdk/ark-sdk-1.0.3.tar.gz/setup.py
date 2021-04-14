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
    init = read("constant.py")
    return VERSION_RE.search(init).group(1)


def get_requirements():
    """Reads the requirements file."""
    requirements = read("requirements.txt")
    return list(requirements.strip().splitlines())


setup(
    name="ark-sdk",
    packages=find_packages(),
    url='https://github.com/vlean/ark-sdk',
    version=get_version(),
    author="vlean",
    author_email='vlean@qq.com',
    maintainer="vlean",
    description="ark sdk",
    long_description=read("README.md"),
    keywords=["ark", "nacos"],
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
