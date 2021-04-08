# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotcoin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dotcoin',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Orlando Ospino Sánchez',
    'author_email': 'oroschz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
