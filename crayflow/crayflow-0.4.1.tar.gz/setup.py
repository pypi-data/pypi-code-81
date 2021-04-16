"""
CRayFlow - easy dataset loading.
"""

from setuptools import setup, find_packages
from codecs import open
import os.path as osp

here = osp.abspath(osp.dirname(__file__))

with open(osp.join(here, 'README.md'), encoding='utf-8') as f:
  long_description=f.read()

version = '0.4.1'

setup(
  name = 'crayflow',

  version=version,

  description="""Yet another neural network toolkit - dataflow module""",

  long_description = long_description,
  long_description_content_type="text/markdown",

  url='https://gitlab.com/craynn/crayflow',

  author='Maxim Borisyak',
  author_email='maximus.been@gmail.com',

  maintainer = 'Maxim Borisyak and contributors',
  maintainer_email = 'maximus.been@gmail.com',

  license='MIT',

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],

  keywords='dataflow',

  packages=find_packages(
    exclude=['contrib', 'examples', 'docs', 'tests']
  ),

  extras_require={
    'test': ['pytest >= 5.3.2'],
  },

  install_requires=[
    'numpy >= 1.18.0',
    'requests >= 2.0.0',
    'craygraph >= 0.3.0'
  ],
)


