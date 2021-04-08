# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scalarstop']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.5,<2.0.0',
 'cloudpickle>=1.6.0,<2.0.0',
 'numpy',
 'pandas',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'tensorflow>=2.3.0']

setup_kwargs = {
    'name': 'scalarstop',
    'version': '0.1.0',
    'description': 'A framework for managing machine learning experiments.',
    'long_description': None,
    'author': 'Neocrym Records Inc',
    'author_email': 'engineering@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
