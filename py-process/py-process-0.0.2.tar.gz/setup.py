#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'py-process',
  packages = ['py_process'],
  version = '0.0.2',
  description = 'engine processs',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/FlavioLionelRita/py-process', # use the URL to the github repo
  download_url = 'https://github.com/FlavioLionelRita/py-process/tarball/0.0.2',
  keywords = ['process', 'business process', 'bpm', 'bpmn','engine' ],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@hotmail.com'  
)