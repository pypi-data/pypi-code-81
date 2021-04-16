# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['partiqle']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.53,<2.0.0']

setup_kwargs = {
    'name': 'partiqle',
    'version': '0.0.0',
    'description': 'DynamoDB PartiQL support for Python',
    'long_description': None,
    'author': 'Seonghyeon Kim',
    'author_email': 'self@seonghyeon.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
