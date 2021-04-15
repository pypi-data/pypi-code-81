#!/usr/bin/env python

import os
from setuptools import setup

# load __version__ without importing anything
_version_file = os.path.join(
    os.path.dirname(__file__),
    'kerfed_api/version.py')
with open(_version_file, 'r') as f:
    # use eval to get a clean string of version from file
    __version__ = eval(f.read().strip().split('=')[-1])

# load README.md as long_description
long_description = ''
if os.path.exists('README.md'):
    with open('README.md', 'r') as f:
        long_description = f.read()

setup(name='kerfed_api',
      version=__version__,
      description='Analyze CAD assemblies using the Kerfed API.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Kerfed Intelligent Manufacturing',
      author_email='api@kerfed.com',
      license='MIT',
      url='https://github.com/kerfed/kerfed-api-python',
      keywords='CAD solidworks geometry quoting manufacturing',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.8',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering'],
      packages=['kerfed_api'],
      install_requires=['requests'],
      extras_require={'all': {'trimesh[easy]',
                              'pandas',
                              'openpyxl',
                              'webcolors'}}
      )
