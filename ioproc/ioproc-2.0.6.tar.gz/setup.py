#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup


__author__ = ["Benjamin Fuchs", "Judith Riehm", "Felix Nitsch", "Jan Buschmann"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "2.0.6"
__maintainer__ = "Felix Nitsch"
__email__ = "ioproc@dlr.de"
__status__ = "Production"


def readme():
      with open('README.md') as f:
            return f.read()


setup(name='ioproc',
      version=__version__,
      description='Framework for data pre- and postprocessing',
      long_description='''ioProc is a light-weight workflow manager for Python ensuring robust, scalable and 
                        reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) 
                        for and in the scientific context of energy systems analysis, however, it is widely 
                        applicable in other scientific fields.
                        ''',
      keywords='workflow management, data pipeline, data science',
      url='https://gitlab.com/dlr-ve/ioproc',
      author=', '.join(__author__),
      author_email=__email__,
      license=__license__,
      packages=['ioproc'],
      install_requires=['arrow', 'pandas', 'frozendict', 'pyyaml', 'click', 'cerberus', 'tables'],
      zip_safe=False,
      include_package_data=True,
      )
