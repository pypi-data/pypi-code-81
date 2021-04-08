# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delphai_company_pages']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'azure-storage-blob>=12.8.0,<13.0.0',
 'networkx>=2.5,<3.0',
 'warcio>=1.7.4,<2.0.0']

setup_kwargs = {
    'name': 'delphai-company-pages',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'delphai',
    'author_email': 'admin@delphai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
