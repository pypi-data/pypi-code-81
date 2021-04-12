# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deutschspiel']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.25,<1.0']

setup_kwargs = {
    'name': 'deutschspiel',
    'version': '0.1.0',
    'description': 'Framework to handle German Grammar',
    'long_description': None,
    'author': 'Marco Menezes',
    'author_email': 'marcoaurelioreislima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
