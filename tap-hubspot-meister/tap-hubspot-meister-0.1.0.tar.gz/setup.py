# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_hubspot_meister', 'tap_hubspot_meister.test']

package_data = \
{'': ['*'], 'tap_hubspot_meister': ['schemas/*']}

install_requires = \
['hubspot-api-client>=3.7.2,<4.0.0',
 'pydash>=5.0.0,<6.0.0',
 'rich>=10.1.0,<11.0.0',
 'singer-python>=5.12.1,<6.0.0',
 'singer>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'tap-hubspot-meister',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Juan Sebastian Suarez Valencia',
    'author_email': 'juan.valencia@meisterlabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
