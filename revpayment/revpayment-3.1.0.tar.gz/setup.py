# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['revpayment',
 'revpayment.invoice',
 'revpayment.invoice.migrations',
 'revpayment.logistics',
 'revpayment.logistics.migrations',
 'revpayment.migrations',
 'revpayment.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.7,<4.0.0',
 'cryptography>=3.4.7,<4.0.0',
 'djangorestframework>=3.12.4,<4.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'revpayment',
    'version': '3.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chien',
    'author_email': 'a0186163@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
