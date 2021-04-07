#!/usr/bin/env python
import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycomma',
    version='0.1.2',
    description='Python library for processing CSV files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JordanKobeWade/pycomma',
    download_url='https://github.com/JordanKobeWade/pycomma/releases',
    author='Sean Hwang',
    author_email='seanphwang@gmail.com',
    license='MIT',
    packages=['pycomma'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ]
)