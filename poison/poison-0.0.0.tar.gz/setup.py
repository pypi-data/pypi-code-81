# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poison']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poison',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
