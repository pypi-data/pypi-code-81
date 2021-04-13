# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rss_parser']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1', 'lxml>=4.5.2', 'pydantic>=1.6.1', 'requests>=2.24.0']

setup_kwargs = {
    'name': 'rss-parser',
    'version': '0.2.0',
    'description': 'Typed pythonic RSS parser',
    'long_description': None,
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
