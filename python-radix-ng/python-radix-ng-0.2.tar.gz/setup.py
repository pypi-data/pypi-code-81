# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='python-radix-ng',
version='0.2',
description='A tool for conversion numbers from one base to another, TheTechRobo edition',
long_description=long_description,
url='https://github.com/valbub/python-radix',
author='valbub, yury-khrustalev, mulkieran, TheTechRobo',
license='MIT',
classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
],
keywords='radix numbers bases number systems base36',
packages=['python_radix'],
install_requires=[],
platforms=['Any'])
