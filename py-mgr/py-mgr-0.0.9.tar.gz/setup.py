#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'py-mgr',
  packages = ['py_mgr'],
  version = '0.0.9',
  description = 'administration of modules and plugin',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/FlavioLionelRita/py-mgr', # use the URL to the github repo
  download_url = 'https://github.com/FlavioLionelRita/py-mgr/tarball/0.0.9',
  keywords = ['manager', 'plugin'],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@hotmail.com'  
)
