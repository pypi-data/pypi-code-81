# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dog']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dog.py',
    'version': '0.2.0',
    'description': 'An API wrapper for https://thedogapi.com/ that covers the full API.',
    'long_description': None,
    'author': 'ToxicKidz',
    'author_email': '78174417+ToxicKidz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
