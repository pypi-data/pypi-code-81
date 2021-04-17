# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tikotapi']
setup_kwargs = {
    'name': 'tikotapi',
    'version': '1.0.5',
    'description': 'The lib for game published in tikotshopgame.tk',
    'long_description': None,
    'author': 'tikotstudio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
