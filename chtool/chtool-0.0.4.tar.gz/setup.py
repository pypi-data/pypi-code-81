from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="chtool",
    version="0.0.4",    
    author="lichanghua",
    author_email="1371214116@qq.com",
    description="工具箱",
    long_description=open("README.rst", encoding="utf8").read(),
 
    url="https://github.com",
    packages=find_packages(),

    install_requires=[
        "pandas >= 0.13",
        "psycopg2-binary",
        ],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
)