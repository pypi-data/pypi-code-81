# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybitespodcast']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.2,<7.0.0']

entry_points = \
{'console_scripts': ['search = pybitespodcast.search:main']}

setup_kwargs = {
    'name': 'pybitespodcast',
    'version': '0.1.0',
    'description': '',
    'long_description': "# PyBites Podcast Searcher\n\nA tool to browse the podcast's RSS feed.\n",
    'author': 'Bob Belderbos',
    'author_email': 'bobbelderbos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bbelderbos/pybitespodcast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
