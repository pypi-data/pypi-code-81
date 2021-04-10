# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rt_pie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rt-pie',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kaspar',
    'author_email': 'kaspar.wolfisberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
