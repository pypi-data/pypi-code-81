# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomad', 'nomad.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pyserde>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'nomad-api',
    'version': '0.0.1',
    'description': 'Hashicorp Nomad API client written in modern Python',
    'long_description': None,
    'author': 'yukinarit',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
