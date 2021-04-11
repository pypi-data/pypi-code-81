# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poit']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'poit',
    'version': '0.1.1',
    'description': 'Fetch information from POIT, The Official Swedish Gazette',
    'long_description': None,
    'author': 'Johan Magnusson',
    'author_email': 'jcmmagnusson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
