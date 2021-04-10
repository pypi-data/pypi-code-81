# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kapla', 'kapla.cli']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'colorama>=0.4.4,<0.5.0',
 'commitizen>=2.14.2,<3.0.0',
 'flake8>=3.9.0,<4.0.0',
 'isort>=5.8.0,<6.0.0',
 'kapla-cli-core>=1.0.0,<2.0.0',
 'mypy>=0.812,<0.813',
 'pre-commit>=2.12.0,<3.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytest>=6.2.3,<7.0.0',
 'twine>=3.4.1,<4.0.0']

entry_points = \
{'console_scripts': ['k = kapla.cli.app:cli', 'repo = kapla.cli.app:cli']}

setup_kwargs = {
    'name': 'kapla-cli',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Guillaume Charbonnier',
    'author_email': 'guillaume.charbonnier@araymond.com',
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
