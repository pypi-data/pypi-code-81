# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osol', 'osol.algorithms', 'osol.tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0', 'scipy>=1.6.2,<2.0.0']

setup_kwargs = {
    'name': 'osol',
    'version': '0.0.10',
    'description': '',
    'long_description': None,
    'author': 'wol4aravio',
    'author_email': 'panovskiy.v@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
