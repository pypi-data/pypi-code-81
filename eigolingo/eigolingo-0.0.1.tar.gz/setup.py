# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eigolingo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['eigo = eigolingo:main', 'hworld = eigolingo:hello_world']}

setup_kwargs = {
    'name': 'eigolingo',
    'version': '0.0.1',
    'description': 'Determine the number of unique words in a given text/string',
    'long_description': None,
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
