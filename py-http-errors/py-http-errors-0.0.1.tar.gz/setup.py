from __future__ import absolute_import, division, print_function
from setuptools import setup

description = "Python Common HTTP Exceptions for API-JSON-Response"

try:
    with open("README.md", "r") as fh:
        readme = fh.read()
except:
    readme = description

setup(
    name="py-http-errors",
    url="https://github.com/dodoru/py-http-errors",
    license="MIT",
    version='0.0.1',
    author="Nico Ning",
    author_email="dodoru@foxmail.com",
    description=(description),
    long_description=readme,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    packages=["py_http_errors"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[],
    platforms='any',
)
