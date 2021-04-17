# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tiff']
setup_kwargs = {
    'name': 'tiff',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Moleque',
    'author_email': 'molecada@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
