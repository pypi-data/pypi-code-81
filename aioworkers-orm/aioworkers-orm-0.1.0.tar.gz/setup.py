# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_orm']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers-databases>=0.1.1,<0.2.0', 'orm>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'aioworkers-orm',
    'version': '0.1.0',
    'description': 'Module to work with orm',
    'long_description': '# aioworkers-orm\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-orm/CI)](https://github.com/aioworkers/aioworkers-orm/actions?query=workflow%3ACI)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-orm)](https://pypi.org/project/aioworkers-orm)\n[![PyPI](https://img.shields.io/pypi/v/aioworkers-orm)](https://pypi.org/project/aioworkers-orm)\n\nAn aioworkers plugin for [orm](https://github.com/encode/orm)\nto add `orm.Model` available via `aioworkers.core.context.Context`.\n\nFeatures:\n- Attach model by class reference.\n- Create model by specification.\n\n## Development\n\nInstall dev requirements:\n\n```shell\npoetry install\n```\n\nRun tests:\n\n```shell\npytest\n```\n',
    'author': 'Alexander Bogushov',
    'author_email': 'abogushov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
