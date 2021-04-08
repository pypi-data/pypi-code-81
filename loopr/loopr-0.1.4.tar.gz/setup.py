# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loopr',
 'loopr.api',
 'loopr.api.annotation',
 'loopr.api.dataset',
 'loopr.api.project',
 'loopr.api.row',
 'loopr.api.urls',
 'loopr.models',
 'loopr.models.entities',
 'loopr.resources',
 'loopr.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'loopr',
    'version': '0.1.4',
    'description': 'A python sdk to interact with loopR APIs.',
    'long_description': None,
    'author': 'LoopR',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
