# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages


requires=['jieba','triedtree']

setup(name='addressformat',
      version='0.4.13',
      install_requires = requires,
      description='地址省市区解析',
      long_description="地址解析模块",
      license="MIT",
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
      ],
      packages=['addressformat', 'addressformat.resources'],

      package_dir={'addressformat': 'addressformat', 'addressformat.resources': 'addressformat/resources',
                   'addressformat.entitywords': "addressformat/entitywords"},
      package_data={'': ['*']},
      include_package_data=True,

      )
