# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['distortion']

package_data = \
{'': ['*']}

install_requires = \
['kornia>=0.4.0,<0.5.0', 'torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'distortion',
    'version': '0.1.17',
    'description': 'Watermark distortions',
    'long_description': None,
    'author': 'tanimutomo',
    'author_email': 'tanimutomo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tanimutomo/watermark-distortions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
