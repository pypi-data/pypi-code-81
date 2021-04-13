# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jedi_language_server']

package_data = \
{'': ['*']}

install_requires = \
['docstring-to-markdown<1.0.0',
 'jedi==0.18.0',
 'pydantic>=1.7,<2.0',
 'pygls>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['listsoft = jedi_language_server.cli:cli']}

setup_kwargs = {
    'name': 'listsoft',
    'version': '0.30.1',
    'description': 'A language server for Jedi!',
    'long_description': '# 

	'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pappasam/jedi-language-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
