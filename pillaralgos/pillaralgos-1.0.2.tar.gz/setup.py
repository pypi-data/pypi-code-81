# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pillaralgos', 'pillaralgos.helpers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0', 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'pillaralgos',
    'version': '1.0.2',
    'description': 'Algorithms for Pillar. Currently includes "mini" algorithms, nothing too sophisticated.',
    'long_description': None,
    'author': 'Peter Gates',
    'author_email': 'pgate89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
