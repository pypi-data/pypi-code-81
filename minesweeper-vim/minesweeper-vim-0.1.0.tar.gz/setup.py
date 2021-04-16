# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minesweeper_vim']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['minesweeper-vim = minesweeper_vim.ui:run']}

setup_kwargs = {
    'name': 'minesweeper-vim',
    'version': '0.1.0',
    'description': 'Curses minesweeper with vim bindings',
    'long_description': None,
    'author': 'Brian Cho',
    'author_email': 'briandcho@yahoo.com',
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
