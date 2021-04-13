from __future__ import absolute_import, division, print_function
from setuptools import setup

description = "Python Common Api Exceptions for HTTP-JSON-Response"

setup(
    name="http_api_exception",
    url="https://github.com/dodoru/pyco-api-exceptions",
    license="MIT",
    version='0.0.2',
    author="Nico Ning",
    author_email="dodoru@foxmail.com",
    description=(description),
    long_description=description,
    long_description_content_type="text/plain",
    zip_safe=False,
    include_package_data=True,
    packages=["http_api_exception"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "flask>=0.10",
    ],
    platforms='any',
)
