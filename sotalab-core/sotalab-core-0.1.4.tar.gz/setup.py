# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sotalab', 'sotalab.core', 'sotalab.core.config', 'sotalab.core.utils']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'sotalab-core',
    'version': '0.1.4',
    'description': 'SotaLab',
    'long_description': '# SotaLab-Core\n',
    'author': 'Ming Yang',
    'author_email': 'ymviv@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
