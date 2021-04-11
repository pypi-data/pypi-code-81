#!/usr/bin/env python3
from setuptools import setup
with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'py-expression-lib-opencv',
  packages = ['py_expression_opencv'],
  version = '0.0.3',
  description = 'lib opencv for expressions',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/FlavioLionelRita/py-expression-lib-opencv', # use the URL to the github repo
  download_url = 'https://github.com/FlavioLionelRita/py-expression-lib-opencv/tarball/0.0.1',
  keywords = ['opencv','lib', 'expression'],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@hotmail.com'  
)