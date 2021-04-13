# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizsdk']

package_data = \
{'': ['*'], 'wizsdk': ['images/*']}

install_requires = \
['Sphinx>=3.4.3,<4.0.0',
 'asyncchain>=0.1.0,<0.2.0',
 'asyncio>=3.4.3,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'wizwalker>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'wizsdk',
    'version': '1.3.6',
    'description': 'API for interacting with and making bots for wizard101',
    'long_description': "# WizSDK\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nWizard101 bot Software Development Kit\nA wrapper for [WizWalker](https://github.com/StarrFox/wizwalker) bundled with many other useful function.\nDesigned to make building bots for farming / questing / bazaar sniping / selling / pet training\n\n## documentation\n\nyou can find the documentation [here](https://underpaiddev1.github.io/wizSDK/)\n\nyou can download these from the gh-pages branch if desired\n\n## install\n\nclone the repo or install from pypi `pip install -U wizsdk`\n\n## discord\n\njoin the offical discord [here](https://discord.gg/D9GRrbDzpt)\n\n## development install\n\nThis package uses [poetry](https://python-poetry.org/)\n\n```shell script\n$ poetry install\n```\n\n## building\n\nYou'll need the dev install (see above) for this to work\n\n### Docs\n\n```shell script\n$ cd docs\n$ make html\n```\n",
    'author': 'Underpaid Dev',
    'author_email': 'underpaiddev1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
