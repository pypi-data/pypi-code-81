# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['greatcirclepaths']

package_data = \
{'': ['*']}

install_requires = \
['healpy>=1.13.0,<2.0.0', 'matplotlib>=3.2.2,<4.0.0', 'pyssht>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'greatcirclepaths',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'Auggie Marignier',
    'author_email': 'augustin.marignier.14@ucl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
