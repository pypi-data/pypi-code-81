#!/usr/bin/env python
from setuptools import setup


REQUIREMENTS = []

setup(name='psgv',
      version=0.1,
      description='Python System Global Variables',
      author='Alex Hagen',
      author_email='alexhagen6@gmail.com',
      url='https://github.com/alexhagen/psgv',
      long_description=open('README.md').read(),
      packages=['psgv'],
      install_requires=REQUIREMENTS,
     )