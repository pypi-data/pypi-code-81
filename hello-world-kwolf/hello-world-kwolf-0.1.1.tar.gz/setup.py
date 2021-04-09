# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hello_world_kwolf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hello-world-kwolf',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Kaspar',
    'author_email': 'redacted@provider.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
