# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotify', 'dotify.models']

package_data = \
{'': ['*'], 'dotify.models': ['schema/*']}

install_requires = \
['moviepy',
 'mutagen',
 'mypy',
 'python-jsonschema-objects',
 'pytube',
 'requests',
 'spotipy',
 'youtube-search-python']

setup_kwargs = {
    'name': 'dotify',
    'version': '0.1.0',
    'description': '🐍🎶 Yet another Spotify Web API Python library',
    'long_description': None,
    'author': 'billsioros',
    'author_email': 'billsioros97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
