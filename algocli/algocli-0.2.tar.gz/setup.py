#!/usr/bin/env python

from setuptools import setup
import algocli



# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='algocli',
      version=algocli.__version__,
      description="print common algorithms to the command line",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Documentation",
      ],
      keywords='algocli algorithms console command line',
      author='Emanuel Ramirez Alsina',
      author_email='eramirez2718@gmail.com',
      maintainer='Emanuel Ramirez Alsina',
      maintainer_email='eramirez2718@gmail.com',
      url='https://github.com/emanuel2718/algocli',
      python_requires='>=3.6',
      license='MIT',
      packages=['algocli'],
      zip_safe=False,
      install_requires=[
          'Pygments',
          'bs4',
          'requests',
          'setuptools',
      ],
      entry_points={
          'console_scripts': [
              'algocli = algocli.algocli:run',
          ]
      }
)
