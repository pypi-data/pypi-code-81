# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jarpyvscode',
 'jarpyvscode.projects',
 'jarpyvscode.projects.templates.python',
 'jarpyvscode.projects.templates.python.app',
 'jarpyvscode.projects.templates.python.pkg',
 'jarpyvscode.projects.templates.python.tests',
 'tests']

package_data = \
{'': ['*'], 'jarpyvscode.projects': ['templates/vsce/*']}

install_requires = \
['black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'json5>=0.9.5,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.2.3,<2.0.0',
 'psutil>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'jarpyvscode',
    'version': '0.2.3',
    'description': "Python backend for Jamil Raichouni's personal Visual Studio Code Extension jamilraichouni.jarpyvscode",
    'long_description': None,
    'author': 'Jamil Raichouni',
    'author_email': 'raichouni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
