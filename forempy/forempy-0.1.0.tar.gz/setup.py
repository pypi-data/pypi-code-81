# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forempy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'forempy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
