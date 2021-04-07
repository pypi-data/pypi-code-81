# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt',
 'dbt.adapters',
 'dbt.adapters.oracle',
 'dbt.include',
 'dbt.include.oracle']

package_data = \
{'': ['*'], 'dbt.include.oracle': ['macros/*', 'macros/materializations/*']}

install_requires = \
['cx-Oracle>=8.1.0,<9.0.0', 'dbt>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'dbt-oracledb',
    'version': '0.1.0',
    'description': 'DBT adapter for Oracle databases',
    'long_description': None,
    'author': 'emacha',
    'author_email': '15370927+emacha@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
