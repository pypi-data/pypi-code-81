# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changelog', 'changelog.cli']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['changelog = changelog.__main__:app']}

setup_kwargs = {
    'name': 'changelog-cmd',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jack Smith',
    'author_email': 'jack.je.smith@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
