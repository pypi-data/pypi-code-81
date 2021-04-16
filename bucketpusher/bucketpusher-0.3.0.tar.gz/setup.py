# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucketpusher']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.30.0,<5.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'cryptography>=3.2.1,<4.0.0',
 'flake8>=3.8.4,<4.0.0',
 'google-auth-oauthlib>=0.4.2,<0.5.0',
 'google-cloud-storage>=1.32.0,<2.0.0',
 'google-crc32c>=1.0.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['bucketpusher = bucketpusher:cli.main']}

setup_kwargs = {
    'name': 'bucketpusher',
    'version': '0.3.0',
    'description': 'Push local files to cloud storage bucket',
    'long_description': None,
    'author': 'Dominic Ward',
    'author_email': 'dom@deeuu.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
