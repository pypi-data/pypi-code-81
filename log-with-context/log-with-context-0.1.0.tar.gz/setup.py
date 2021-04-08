# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['log_with_context']
setup_kwargs = {
    'name': 'log-with-context',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'James Mishra',
    'author_email': 'james.mishra@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
