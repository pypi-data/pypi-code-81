# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fibsem_metadata', 'fibsem_metadata.multiscale']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'fibsem-metadata',
    'version': '0.1.0',
    'description': 'Metadata and metadata generators for FIB-SEM data',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7,<4',
}


setup(**setup_kwargs)
