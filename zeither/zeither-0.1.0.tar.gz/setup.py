# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeither']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zeither',
    'version': '0.1.0',
    'description': 'A either python package (study purpose)',
    'long_description': None,
    'author': 'tba',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
