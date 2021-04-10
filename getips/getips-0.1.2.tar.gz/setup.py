# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getips']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'funcy>=1.15,<2.0']

entry_points = \
{'console_scripts': ['getips = getips.cli:main']}

setup_kwargs = {
    'name': 'getips',
    'version': '0.1.2',
    'description': 'Small python tool to get all IP addresses from list of domains.',
    'long_description': None,
    'author': 'n4Zz2',
    'author_email': 'root@n4Zz2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
