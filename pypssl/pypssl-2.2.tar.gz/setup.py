# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypssl']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pssl = bin.pssl:main']}

setup_kwargs = {
    'name': 'pypssl',
    'version': '2.2',
    'description': 'Python API for PSSL.',
    'long_description': 'Client API for PSSL\n===================\n\nClient API to query the Passive SSL implementation provided by CIRCL.\n\nPassive SSL Services\n====================\n\n* (default) [CIRCL Passive SSL](http://circl.lu/services/passive-ssl/)\n\n\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adulau/crl-monitor/tree/master/client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
