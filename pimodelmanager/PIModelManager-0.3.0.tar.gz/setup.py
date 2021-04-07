# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pimodelmanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pimodelmanager',
    'version': '0.3.0',
    'description': 'A package used to manage our ML models.',
    'long_description': '# Introduction \nA python package providing a singleton ModelManager class. \n\n# Getting Started\n1.\tInstall: pip install PIModelManager\n2.\tImport: from PIModelManager import ModelManager\n3.\tSet credentials: ModelManager().set_credentials(...)',
    'author': 'Martin Kirilov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
