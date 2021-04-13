# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texpj']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['texpj = texpj:main']}

setup_kwargs = {
    'name': 'texpj',
    'version': '0.1.0',
    'description': 'Utilidad para mantener plantillas de latex',
    'long_description': None,
    'author': 'Benyamin Galeano',
    'author_email': 'benyamin.galeano@galileo.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
