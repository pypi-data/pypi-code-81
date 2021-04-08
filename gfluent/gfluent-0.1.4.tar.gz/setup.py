# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gfluent']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=2.13.1,<3.0.0']

setup_kwargs = {
    'name': 'gfluent',
    'version': '0.1.4',
    'description': 'A fluent API for Google Cloud Python Client',
    'long_description': None,
    'author': 'Zhong Dai',
    'author_email': 'zhongdai.au@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
