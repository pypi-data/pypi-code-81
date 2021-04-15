# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ubase']
install_requires = \
['aiosqlite>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'ubase',
    'version': '0.1.3',
    'description': 'μBase is oversimpistic key-value database wrapper on top of aiosqlite',
    'long_description': None,
    'author': 'Grigory Bakunov',
    'author_email': 'thebobuk@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
