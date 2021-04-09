# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyespremclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyespremclient',
    'version': '0.1.3',
    'description': 'A python module for ESPREM clients',
    'long_description': None,
    'author': 'Zafar Iqbal',
    'author_email': 'ultrasine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
