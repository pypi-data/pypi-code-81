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
    'version': '0.1.3',
    'description': 'Convert YouTube videos to Anki decks.',
    'long_description': '# youtube-to-anki\n\nConverts a YouTube video into Anki Cards.\n\nTakes a YouTube video with audio in your target language and transcript (subtitles) in your native language and converts it into an `.apkg` file that can easily be imported into Anki. The Anki cards have the target language audio on the front and the native language transcript on the back. I hope this helps improving your listening comprehension.\n\n## Installation\n\n### PyPI\n\n```\npip install youtube-to-anki\n```\n\nNote: When you install this package though `pip`, you will have to manually install [ffmpeg](https://ffmpeg.org/download.html) afterwards. One easy way to accomplish this is with [conda](https://docs.conda.io/en/latest/).\n\n```\nconda create --name youtube-to-anki ffmpeg pip\nconda activate youtube-to-anki\npip install youtube-to-anki\nyoutube-to-anki --help\n```\n\n### Conda\n\nComing soon ...\n\n## Usage\n\n### CLI\n\nYou can use the command like interface like this:\n\n```\nyoutube-to-anki <video_id>\n```\n\nWhere `<video_id>` can be extracted from a YouTube URL like this:\n\n`https://www.youtube.com/watch?v=<video_id>`\n\nThere are some CLI options you can provide, for example for choosing the transcript language. Check `youtube-to-anki --help` for details.\n\n## Importing to Anki\n\nyoutube-to-anki produces an `.apkg` file, which can easily be imported into Anki. In Anki, just click "File" -> "Import".\n\n## Listing Available Transcripts\n\nyoutube-to-anki calls [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for requesting the video transcripts. If you\'re unsure what value to provide to the `--transcript-language` option, you can list all available languages with `youtube_transcript_api --list-transcripts <video_id>`.\n',
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
