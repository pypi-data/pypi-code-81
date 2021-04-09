# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_inout']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'drf-inout',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Hloska',
    'author_email': 'martin.hloska@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
