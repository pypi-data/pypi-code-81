# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_hplc']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'py-hplc',
    'version': '0.1.0',
    'description': 'An unoffical Python wrapper for the SSI-Teledyne Next Generation class HPLC pumps.',
    'long_description': None,
    'author': 'Alex W',
    'author_email': 'alex@southsun.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teauxfu/py-hplc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
