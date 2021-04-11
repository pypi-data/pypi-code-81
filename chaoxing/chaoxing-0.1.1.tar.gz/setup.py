# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaoxing']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'chaoxing',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'lisonge',
    'author_email': 'i@songe.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
