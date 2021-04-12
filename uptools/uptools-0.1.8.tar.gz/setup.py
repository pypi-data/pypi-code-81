# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uptools']

package_data = \
{'': ['*']}

install_requires = \
['seutils>=0,<1', 'uproot-methods>=0.9.2,<0.10.0', 'uproot3>=3.14.4,<4.0.0']

setup_kwargs = {
    'name': 'uptools',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Thomas Klijnsma',
    'author_email': 'tklijnsm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
