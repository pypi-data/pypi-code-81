# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['denise']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['denise = denise.denise:start']}

setup_kwargs = {
    'name': 'denise',
    'version': '0.1.1',
    'description': 'A package containing love',
    'long_description': '',
    'author': 'Matthew Jones',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
