import codecs
import os
import sys
from setuptools import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "pyhtmllib"
PACKAGES = ["HtmlLib", ]
DESCRIPTION = "HtmlLib is a free python package, using to discribe html page with Python."
LONG_DESCRIPTION = read("README.txt")
KEYWORDS = "html web front-end"
AUTHOR = "PointCode Organization"
AUTHOR_EMAIL = "pointcode@126.com"
URL = "https://gitee.com/albert_zhong/htmllib/tree/master/"
VERSION = "1.0-beta"
LICENSE = "Apache-2.0"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)