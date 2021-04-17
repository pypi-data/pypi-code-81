# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunsync']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dunsync',
    'version': '0.1.0',
    'description': 'Identical to unsync, but supports cpu-bound continuation functions',
    'long_description': None,
    'author': 'Daniel Hjertholm',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
