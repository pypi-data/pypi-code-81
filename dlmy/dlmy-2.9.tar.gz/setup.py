# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlmy']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'colorama>=0.4.4,<0.5.0',
 'configparser>=5.0.1,<6.0.0',
 'lxml>=4.6.2,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'youtube_dl>=2021.1.8,<2022.0.0']

entry_points = \
{'console_scripts': ['dlmy = dlmy.__main__:main']}

setup_kwargs = {
    'name': 'dlmy',
    'version': '2.9',
    'description': 'Yet another Spotify Downloader ...',
    'long_description': '## Dlmy\n\n### Introduction\n\nYet another Spotify Downloader omg. 🤐\n\nDlmy uses the given Spotify Track\'s metadata tags, to extract information about the music. After extracting information, the music is downloaded from YouTube using [youtube_dl](https://github.com/ytdl-org/youtube-dl).\n\nAny contributions are welcomed!\n\n### Features\n\n- [x] Download single tracks using a Spotify url\n- [x] Download single tracks using a search query\n- [x] Download whole Spotify playlists\n\n### Installation\n\n#### Dependencies\n\nThe only dependency is `ffmpeg`, to embed metadata to tracks.\nIf you wish to skip this you can change `ffmpeg=True` to `ffmpeg=False` in in the configuration file.\n\n#### Packages\n\n##### Pip\n\n```bash\npip install dlmy\n```\n\n### Usage\n\n```bash\ndlmy -t "title of the track"        download a track using query\ndlmy -t <url>                       download the given track\ndlmy -l <url>                       download a whole playlist\n```\n',
    'author': 'yrwq',
    'author_email': 'yrwqid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
