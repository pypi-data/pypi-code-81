#!/usr/bin/env python

import os
from distutils.core import setup
from setuptools import find_packages

setup(
    data_files = [
        (os.path.join('lib', 'osc-plugins'), ['clone.py']),
    ]
)
