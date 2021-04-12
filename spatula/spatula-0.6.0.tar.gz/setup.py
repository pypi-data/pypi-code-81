# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spatula']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx[docs]>=3.4.3,<4.0.0',
 'attrs[attrs]>=20.3.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'ipython[shell]>=7.19.0,<8.0.0',
 'lxml>=4.6.2,<5.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'scrapelib>=2.0.2,<3.0.0',
 'sphinx-click[docs]>=2.5.0,<3.0.0',
 'sphinx-rtd-theme[docs]>=0.5.1,<0.6.0']

entry_points = \
{'console_scripts': ['spatula = spatula.cli:cli']}

setup_kwargs = {
    'name': 'spatula',
    'version': '0.6.0',
    'description': 'lightweight structured scraping toolkit',
    'long_description': '# spatula\n\n**spatula** is a lightweight scraping framework, designed to encourage best practices and ease development and testing of scrapers.\n\n[![PyPI version](https://badge.fury.io/py/spatula.svg)](https://badge.fury.io/py/spatula)\n\n[![Test & Lint](https://github.com/jamesturk/spatula/workflows/Test%20&%20Lint/badge.svg)](https://github.com/jamesturk/spatula/actions?query=workflow%3A%22Test+%26+Lint%22)\n\n[![](https://readthedocs.org/projects/spatula/badge/?version=latest&style=flat)](https://spatula.readthedocs.org)\n',
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jamesturk/spatula/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
