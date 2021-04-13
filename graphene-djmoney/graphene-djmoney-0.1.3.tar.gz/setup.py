# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_djmoney', 'graphene_djmoney.schema']

package_data = \
{'': ['*']}

install_requires = \
['Django>2',
 'django-money>=1.1,<2.0',
 'graphene-django>=2',
 'graphene<3',
 'psycopg2-binary>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'graphene-djmoney',
    'version': '0.1.3',
    'description': 'GraphQL Money types for Django using graphene and django-money (djmoney).',
    'long_description': None,
    'author': 'Paul Craciunoiu',
    'author_email': 'paul@craciunoiu.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
