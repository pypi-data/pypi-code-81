# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtube_to_anki', 'youtube_to_anki.youtube']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0',
 'genanki>=0.10,<0.11',
 'pydub>=0.25,<0.26',
 'youtube_dl==2021.04.07',
 'youtube_transcript_api>=0.4,<0.5']

entry_points = \
{'console_scripts': ['youtube-to-anki = youtube_to_anki.main:main']}

setup_kwargs = {
    'name': 'youtube-to-anki',
    'version': '0.1.1',
    'description': 'Convert YouTube videos to Anki decks.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
