# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['patcheck']
entry_points = \
{'console_scripts': ['APPLICATION-NAME = patcheck:main']}

setup_kwargs = {
    'name': 'patcheck',
    'version': '1.12.0',
    'description': 'A CLI tool to validate user permission on the given BigQuery datasets, and return validation result as a csv file `check_result.csv`',
    'long_description': None,
    'author': 'Worasit Daimongkol',
    'author_email': 'worasit.daimongkol@refinitiv.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
