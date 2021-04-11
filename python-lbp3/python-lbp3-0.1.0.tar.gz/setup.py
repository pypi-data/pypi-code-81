# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_lbp3']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0', 'httpx']

setup_kwargs = {
    'name': 'python-lbp3',
    'version': '0.1.0',
    'description': 'A Python API wrapper for the LBP3 datastore',
    'long_description': None,
    'author': 'Matt Gosden',
    'author_email': 'mdgosden@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
