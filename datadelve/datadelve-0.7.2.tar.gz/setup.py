# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadelve']

package_data = \
{'': ['*']}

install_requires = \
['jsonpointer>=2.0,<3.0']

setup_kwargs = {
    'name': 'datadelve',
    'version': '0.7.2',
    'description': 'A library to read and manipulate nested data structures, particularly ones read from JSON files',
    'long_description': None,
    'author': 'Nick Thurmes',
    'author_email': 'nthurmes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
