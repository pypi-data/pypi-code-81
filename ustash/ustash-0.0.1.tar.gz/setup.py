#!/usr/bin/env python3
# -*- coding: utf-8 *-*

##
# With credit to the PyPA and their fine work, this setup.py is based
# upon the example project found here:
#
#   https://github.com/pypa/sampleproject
##

from setuptools import setup, find_packages

import pathlib

# Path to top-level source directory
here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
  # Package name
  name = 'ustash',

  # Version
  version = '0.0.1',

  # Short one-line description
  description = 'Web-based personal data stash/store',

  # Long description slurped from top-level README.md
  long_description = long_description,
  long_description_content_type = 'text/markdown',

  # Project URLs
  url = 'https://github.com/destinatech/ustash',
  project_urls = {
    'Bug Reports': 'https://github.com/destinatech/ustash/issues',
    'Source': 'https://github.com/destinatech/ustash',
  },

  # Author details
  author = 'Francis M',
  author_email = 'francis@vnet.destinatech.com',

  # PyPI classifiers (see https://pypi.org/classifiers/)
  classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
  ],

  # Keywords to be listed on PyPI entry
  keywords = 'ustash,web,based,personal,data,stash,store,storage',

  # Where to find source files for the ustash package
  package_dir = {'': 'src'},
  packages = find_packages(where='src'),

  # Additional data files to distribute
  package_data = {'ustash': ['py.typed']},

  # Dependencies
  python_requires = '>=3.8, <4',
  install_requires = [],

  # Test suite
  test_suite = 'nose.controller',
  tests_require = ['nose'],
)

##
# vim: ts=2 sw=2 et fdm=marker :
##
