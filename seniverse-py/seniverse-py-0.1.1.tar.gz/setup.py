# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seniverse']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'seniverse-py',
    'version': '0.1.1',
    'description': '心知天气第三方SDK / seniverse third party sdk for python3',
    'long_description': None,
    'author': 'weak_ptr',
    'author_email': 'weak_ptr@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
