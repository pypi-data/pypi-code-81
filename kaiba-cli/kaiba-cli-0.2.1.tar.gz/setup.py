# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaiba_cli']

package_data = \
{'': ['*']}

install_requires = \
['kaiba>=0.2.1,<0.3.0',
 'returns>=0.14.0,<0.15.0',
 'simplejson>=3.17.2,<4.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['kaiba = kaiba_cli.cli:main']}

setup_kwargs = {
    'name': 'kaiba-cli',
    'version': '0.2.1',
    'description': 'Kaiba Json Transformer CLI',
    'long_description': None,
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
