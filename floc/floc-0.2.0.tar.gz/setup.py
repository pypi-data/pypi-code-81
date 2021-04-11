# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['floc', 'floc.floc_go']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'floc',
    'version': '0.2.0',
    'description': 'A floc simulator wrapper for Python over a Go implementation',
    'long_description': '# FLoC\n\n<p align="center">\n    <a href="https://github.com/thepabloaguilar/floc/actions?query=workflow%3Atest"><img alt="Build Status" src="https://github.com/thepabloaguilar/floc/workflows/test/badge.svg?branch=main"></a>\n    <a href="https://floc.readthedocs.io/en/latest/?badge=latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/floc/badge/?version=latest"></a>\n    <a href="https://pypi.org/project/floc/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/floc.svg"></a>\n    <a href="https://codecov.io/gh/thepabloaguilar/floc"><img alt="Coverage Status" src="https://codecov.io/gh/thepabloaguilar/floc/branch/main/graph/badge.svg"></a>\n    <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>\n    <a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="https://img.shields.io/badge/mypy-checked-2a6db2"></a>\n    <a href="https://github.com/wemake-services/wemake-python-styleguide"><img alt="wemake python styleguide" src="https://img.shields.io/badge/style-wemake-000000.svg"></a>\n</p>\n\n---\n\n## Introduction\n\nThis is a Python wrapper of [this](https://github.com/shigeki/floc_simulator) implementation for FLoC written in go!\n\nIt\'s easy to calculate the CohortID using this lib, see the example below:\n\n```python\n>>> from floc import simulate\n>>> host_list = [\n...     \'www.nikkei.com\',\n...     \'jovi0608.hatenablog.com\',\n...     \'www.nikkansports.com\',\n...     \'www.yahoo.co.jp\',\n...     \'www.sponichi.co.jp\',\n...     \'www.cnn.co.jp\',\n...     \'floc.glitch.me\',\n...     \'html5.ohtsu.org\',\n... ]\n>>> simulate(host_list)\n21454\n```\n\nBy default, we\'ll use the `SortingLshClusters` from FLoC\'s `1.0.6` version. If you want to use other, just pass it to the function:\n\n```python\n>>> from floc import simulate\n>>> host_list = [\n...     \'www.nikkei.com\',\n...     \'jovi0608.hatenablog.com\',\n...     \'www.nikkansports.com\',\n...     \'www.yahoo.co.jp\',\n...     \'www.sponichi.co.jp\',\n...     \'www.cnn.co.jp\',\n...     \'floc.glitch.me\',\n...     \'html5.ohtsu.org\',\n... ]\n>>> sorting_cluster_data = "" # READ THE DATA FROM SOMEWHERE\n>>> simulate(host_list, sorting_cluster_data)\n21454\n```\n\nWe also expose some other functions, see the documentation [here](https://floc.readthedocs.io)\n',
    'author': 'Pablo Aguilar',
    'author_email': 'pablo.aguilar@fatec.sp.gov.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thepabloaguilar/floc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
