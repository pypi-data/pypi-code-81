# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptdt']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'ptdt',
    'version': '0.1.4',
    'description': 'PyTorch Debug Tools',
    'long_description': None,
    'author': 'tanimutomo',
    'author_email': 'tanimutomo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tanimutomo/ptdt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
