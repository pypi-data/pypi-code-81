# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cutout']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0']

setup_kwargs = {
    'name': 'cut-out-cookies',
    'version': '0.1.0',
    'description': 'Jinja extension for optionally including files and directories',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
