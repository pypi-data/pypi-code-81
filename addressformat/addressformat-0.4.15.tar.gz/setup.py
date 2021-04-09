# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages


requires=['jieba','triedtree']

setup(name='addressformat',
      version='0.4.15',
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
      packages=find_packages(),
      include_package_data=True,
      package_data={'addressformat': ['addressformat/resources/*','addressformat/entitywords/*']},

      )
