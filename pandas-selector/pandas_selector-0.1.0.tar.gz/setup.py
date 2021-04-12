# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_selector']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1,<2']

setup_kwargs = {
    'name': 'pandas-selector',
    'version': '0.1.0',
    'description': 'Simple column selector for loc[], iloc[], assign and others.',
    'long_description': None,
    'author': 'Eike von Seggern',
    'author_email': 'eike@vonseggern.space',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
