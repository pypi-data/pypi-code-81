# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iliad']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['iliad = iliad.cli:cli']}

setup_kwargs = {
    'name': 'iliad',
    'version': '0.4.0',
    'description': 'A monorepo tool for Poetry',
    'long_description': '# iliad\nA monorepo tool for [Poetry](https://github.com/python-poetry/poetry)\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/iliad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
