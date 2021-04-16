# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['distvis']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'distvis',
    'version': '0.1.2',
    'description': 'Distribution of data visualizations for insights, feature engineering and debugging',
    'long_description': None,
    'author': 'milo.iturra',
    'author_email': 'iturra.camilo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
