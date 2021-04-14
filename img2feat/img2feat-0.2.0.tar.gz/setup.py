#!/usr/bin/env python
# -*- coding: utf-8 -*-

# convert README.md to README.rst
# % pandoc --from markdown --to rst README.md -o README.rst

# make distribution
# % python setup.py sdist bdist_wheel

# upload to pypi
# % twine upload --repository pypi dist/*

# uninstall
# % python setup.py install --record installed_files
# % cat installed_files | xargs rm -rf
# % rm installed_files

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name= 'img2feat', # Application name:
    version= '0.2.0', # Version number

    author= 'Masayuki Tanaka', # Author name
    author_email= 'mastnk@gmail.com', # Author mail

    url='https://github.com/mastnk/img2feat', # Details
    description='Convert image to feature based on convolutional neural network (CNN).', # short description
    long_description=read('README.rst'), # long description
    install_requires=[ # Dependent packages (distributions)
      'scikit-learn', 'numpy', 'torch', 'torchvision','opencv-python', 'scikit-build', 'cmake', 'scipy',
    ],

    include_package_data=False, # Include additional files into the package
    packages=find_packages(exclude=('tests')),

    test_suite = 'tests',

    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3.6',
    ]
)

