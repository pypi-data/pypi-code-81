# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forallpeople']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'forallpeople',
    'version': '2.0.5',
    'description': 'SI units library for daily calculation work intended for daily calculation work',
    'long_description': None,
    'author': 'Connor Ferster',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
