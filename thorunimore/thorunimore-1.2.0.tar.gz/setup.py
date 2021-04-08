# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thorunimore',
 'thorunimore.database',
 'thorunimore.database.base',
 'thorunimore.telegram',
 'thorunimore.web']

package_data = \
{'': ['*'], 'thorunimore.web': ['static/*', 'templates/*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'authlib>=0.14.3,<0.15.0',
 'coloredlogs>=14.0,<15.0',
 'flask-sqlalchemy>=2.4.4,<3.0.0',
 'flask>=1.1.2,<2.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'royalnet==6.0.0a4',
 'telethon>=1.16.4,<2.0.0']

setup_kwargs = {
    'name': 'thorunimore',
    'version': '1.2.0',
    'description': 'A moderator bot for the Unimore Informatica group',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
