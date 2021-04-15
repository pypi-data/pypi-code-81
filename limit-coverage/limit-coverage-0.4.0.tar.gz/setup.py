# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['limit_coverage']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['limit-coverage = limit_coverage:main']}

setup_kwargs = {
    'name': 'limit-coverage',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Max W Chase',
    'author_email': 'max.chase@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
