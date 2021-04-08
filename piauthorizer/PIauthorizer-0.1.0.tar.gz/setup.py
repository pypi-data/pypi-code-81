# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piauthorizer',
 'piauthorizer.authorization',
 'piauthorizer.autorest',
 'piauthorizer.functional']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.0.1,<3.0.0', 'aiohttp>=3.7.4,<4.0.0', 'fastapi>=0.63.0,<0.64.0']

setup_kwargs = {
    'name': 'piauthorizer',
    'version': '0.1.0',
    'description': 'A package to create a uniform authorization and autorest standard for FastAPI',
    'long_description': None,
    'author': 'David Berenstein',
    'author_email': 'david.berenstein@pandoraintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
