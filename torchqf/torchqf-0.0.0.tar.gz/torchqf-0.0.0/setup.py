# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchqf']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'torchqf',
    'version': '0.0.0',
    'description': 'PyTorch Quant Finance',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki.0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.13,<4.0.0',
}


setup(**setup_kwargs)
