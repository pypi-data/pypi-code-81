# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stethoscope_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stethoscope-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Vaccaro',
    'author_email': 'atvaccaro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
