# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aisdk']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10,<0.11']

setup_kwargs = {
    'name': 'aisdk',
    'version': '0.1.0',
    'description': 'The description of the package',
    'long_description': '',
    'author': 'Jose Luis Rosado',
    'author_email': 'jlrosado@ferrovial.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-poetry/poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
