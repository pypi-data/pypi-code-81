# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dog.py',
    'version': '0.1.0',
    'description': 'An API wrapper for https://thedogapi.com/ that covers the full API.',
    'long_description': None,
    'author': 'ToxicKidz',
    'author_email': '78174417+ToxicKidz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
