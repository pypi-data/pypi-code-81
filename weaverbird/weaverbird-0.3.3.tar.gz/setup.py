# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weaverbird', 'weaverbird.steps', 'weaverbird.utils']

package_data = \
{'': ['*']}

install_requires = \
['numexpr>0', 'pandas>0', 'pydantic>0']

setup_kwargs = {
    'name': 'weaverbird',
    'version': '0.3.3',
    'description': 'Pandas engine for weaverbird data pipelines',
    'long_description': None,
    'author': 'Toucan Toco',
    'author_email': 'dev+weaverbird@toucantoco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
