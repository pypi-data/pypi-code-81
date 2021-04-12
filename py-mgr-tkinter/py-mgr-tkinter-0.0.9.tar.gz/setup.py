#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'py-mgr-tkinter',
  packages = ['py_mgr_tkinter'],
  version = '0.0.9',
  description = 'lib tkinter for py-mgr',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/FlavioLionelRita/py-mgr-tkinter', # use the URL to the github repo
  download_url = 'https://github.com/FlavioLionelRita/py-mgr-tkinter/tarball/0.0.1',
  keywords = ['manager', 'plugin','tkinter'],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@hotmail.com'  
)
