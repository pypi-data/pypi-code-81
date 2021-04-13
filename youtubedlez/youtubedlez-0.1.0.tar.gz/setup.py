# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtubedlez']

package_data = \
{'': ['*']}

install_requires = \
['youtube_dl']

setup_kwargs = {
    'name': 'youtubedlez',
    'version': '0.1.0',
    'description': 'A fast and easy way to use YoutubeDL',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
