# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alastria_identity',
 'alastria_identity.examples',
 'alastria_identity.services',
 'alastria_identity.tests']

package_data = \
{'': ['*']}

install_requires = \
['pyjwt>=1.7.1,<2.0.0',
 'pytest>=6.1.1,<7.0.0',
 'requests>=2.24.0,<3.0.0',
 'web3>=5.12.2,<6.0.0']

setup_kwargs = {
    'name': 'alastria-identity',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Javier Aguirre',
    'author_email': 'javi@wealize.digital',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
