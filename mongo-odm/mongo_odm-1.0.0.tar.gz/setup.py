# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongo_odm']

package_data = \
{'': ['*']}

install_requires = \
['motor>=2.1.0,<2.4.0', 'pydantic>=1.6.0,<1.9.0']

setup_kwargs = {
    'name': 'mongo-odm',
    'version': '1.0.0',
    'description': 'Python async mongodb ODM using motor and pydantic',
    'long_description': '# mongo_odm\n\n<p align="center">\n    <em>Python async mongodb ODM based on motor and pydantic</em>\n</p>\n\n',
    'author': 'Ramzi Tannous',
    'author_email': 'ramzi271996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
