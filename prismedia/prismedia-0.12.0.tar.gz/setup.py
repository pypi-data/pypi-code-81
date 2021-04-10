# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prismedia']

package_data = \
{'': ['*'],
 'prismedia': ['config/*',
               'samples/cli_nfo.txt',
               'samples/cli_nfo.txt',
               'samples/cli_nfo.txt',
               'samples/cli_nfo.txt',
               'samples/cli_nfo.txt',
               'samples/full_nfo_examples.txt',
               'samples/full_nfo_examples.txt',
               'samples/full_nfo_examples.txt',
               'samples/full_nfo_examples.txt',
               'samples/full_nfo_examples.txt',
               'samples/nfo.txt',
               'samples/nfo.txt',
               'samples/nfo.txt',
               'samples/nfo.txt',
               'samples/nfo.txt',
               'samples/samples.txt',
               'samples/samples.txt',
               'samples/samples.txt',
               'samples/samples.txt',
               'samples/samples.txt',
               'samples/yourvideo.txt',
               'samples/yourvideo.txt',
               'samples/yourvideo.txt',
               'samples/yourvideo.txt',
               'samples/yourvideo.txt']}

install_requires = \
['Unidecode>=1.0.23',
 'clint>=0.5.1',
 'configparser>=3.7.1',
 'docopt>=0.6.2',
 'future>=0.17.1',
 'google-api-python-client>=1.7.6',
 'google-auth-httplib2>=0.0.3',
 'google-auth-oauthlib>=0.2.0',
 'google-auth>=1.6.1',
 'httplib2>=0.12.1',
 'oauthlib>=2.1.0',
 'requests-oauthlib>=0.8.0',
 'requests-toolbelt>=0.9.1',
 'requests>=2.18.4',
 'schema>=0.7.1',
 'tzlocal>=1.5.1',
 'uritemplate>=3.0.0',
 'urllib3>=1.22']

entry_points = \
{'console_scripts': ['prismedia = prismedia.upload:main',
                     'prismedia-init = prismedia.genconfig:genconfig']}

setup_kwargs = {
    'name': 'prismedia',
    'version': '0.12.0',
    'description': 'scripting your way to upload videos on peertube and youtube',
    'long_description': '# Prismedia\n\nScripting your way to upload videos to peertube and youtube. Works with Python 3.5+.\n\n[TOC]: #\n\n## Table of Contents\n- [Installation](#installation-and-upgrade)\n  - [From pip](#from-pip)\n  - [From source](#from-source)\n- [Configuration](#configuration)\n  - [Peertube](#peertube)\n  - [Youtube](#youtube)\n- [Usage](#usage)\n- [Enhanced use of NFO](#enhanced-use-of-nfo)\n- [Strict check options](#strict-check-options)\n- [Features](#features)\n- [Compatibility](#compatibility)\n- [Inspirations](#inspirations)\n- [Contributors](#contributors)\n\n## Installation and upgrade\n\n### From pip\n\nSimply install with\n```sh\npip install prismedia\n```\n\nUpgrade with\n```sh\npip install --upgrade prismedia\n```\n\n### From source\n\nGet the source:\n```sh\ngit clone https://git.lecygnenoir.info/LecygneNoir/prismedia.git prismedia\n```\n\nYou may use pip to install requirements: `pip install -r requirements.txt` if you want to use the script directly.  \n(**note:** requirements are generated via `poetry export -f requirements.txt`)\n\nOtherwise, you can use [poetry](https://python-poetry.org), which create a virtualenv for the project directly  \n(Or use the existing virtualenv if one is activated)\n\n```sh\npoetry install\n```\n\n\n## Configuration\n\nGenerate configuration files by running `prismedia-init`.\n\nThen, edit them to fill your credential as explained below. \n\n### Peertube\nConfiguration is in **peertube_secret** file.  \nYou need your usual credentials and Peertube instance URL, in addition with API client_id and client_secret.  \n\nYou can get client_id and client_secret by logging in your peertube instance and reaching the URL:  \nhttps://domain.example/api/v1/oauth-clients/local  \n\n*Alternatively, you can set ``OAUTHLIB_INSECURE_TRANSPORT`` to 1 if you do not use https (not recommended)*\n\n### Youtube\nConfiguration is in **youtube_secret.json** file.  \nYoutube uses combination of oauth and API access to identify.\n\n**Credentials**\nThe first time you connect, prismedia will open your browser to ask you to authenticate to\nYoutube and allow the app to use your Youtube channel.  \n**It is here you choose which channel you will upload to**.  \nOnce authenticated, the token is stored inside the file `.youtube_credentials.json`.  \nPrismedia will try to use this file at each launch, and re-ask for authentication if it does not exist.\n\n**Oauth**:  \nThe default youtube_secret.json should allow you to upload some videos.  \nIf you plan a larger usage, please consider creating your own youtube_secret file:\n\n - Go to the [Google console](https://console.developers.google.com/).\n - Create project.\n - Side menu: APIs & auth -> APIs\n - Top menu: Enabled API(s): Enable all Youtube APIs.\n - Side menu: APIs & auth -> Credentials.\n - Create a Client ID: Add credentials -> OAuth 2.0 Client ID -> Other -> Name: prismedia1 -> Create -> OK\n - Download JSON: Under the section "OAuth 2.0 client IDs". Save the file to your local system.\n - Save this JSON as your youtube_secret.json file.\n\n## Usage\nSupport only mp4 for cross compatibility between Youtube and Peertube.  \n**Note that all options may be specified in a NFO file!** (see [Enhanced NFO](#enhanced-use-of-nfo))\n\nHere are some demonstration of main usage:\n\nUpload a video:\n```sh\nprismedia --file="yourvideo.mp4"\n```\n\nSpecify description and tags:\n```sh\nprismedia --file="yourvideo.mp4" -d "My supa description" -t "tag1,tag2,foo"\n```\n\nProvide a thumbnail:\n```sh\nprismedia --file="yourvideo.mp4" -d "Video with thumbnail" --thumbnail="/path/to/your/thumbnail.jpg"\n```\n\nPublish on Peertube only, while using a channel and a playlist, creating them if they do not exist:\n```sh\nprismedia --file="yourvideo.mp4" --platform=peertube --channel="Cooking recipes" --playlist="Cake recipes" --channelCreate --playlistCreate\n```\n\nUse a NFO file to specify your video options:  \n(See [Enhanced NFO](#enhanced-use-of-nfo) for more precise example)\n```sh\nprismedia --file="yourvideo.mp4" --nfo /path/to/your/nfo.txt\n```\n\nUse some credits to show some activity for you apikey so the platform know it is used and would not put your quota to 0 (only Youtube currently).\n\nTo prevent Youtube from inactivating your apikey after 90days of inactivity it is recommended to launch this command automatically from a script around once a month. It will mwke a call to use a few credits from your daily quota.\nOn Linux and MacOS, you can use cron, on Windows the "Task Scheduler".\n```sh\nprismedia --hearthbeat\n```\n\nTake a look at all available options with `--help`!\n```sh\nprismedia --help\n```\n\n## Enhanced use of NFO\nSince Prismedia v0.9.0, the NFO system has been improved to allow hierarchical loading.\nFirst, **if you already used nfo**, either with `--nfo` or by using `videoname.txt`, nothing changes :-)\n\nBut you are now able to use a more flexible NFO system, by using priorities. This allows you to set some defaults to avoid recreating a full nfo for each video\n\nBasically, Prismedia will now load options in this order, using the last value found in case of conflict:  \n`nfo.txt < directory_name.txt < video_name.txt < command line NFO < command line argument`\n\nYou\'ll find a complete set of samples in the [prismedia/samples](prismedia/samples) directory so let\'s take it as an example:\n```sh\n$ tree Recipes/\nRecipes/\n├── cli_nfo.txt\n├── nfo.txt\n├── samples.txt\n├── yourvideo1.mp4\n├── yourvideo1.txt\n├── yourvideo1.jpg\n├── yourvideo2.mp4\n└── yourvideo2.txt\n```\n\nBy using\n```sh\nprismedia --file=/path/to/Recipes/yourvideo1.mp4 --nfo=/path/to/Recipes/cli_nfo.txt --cca\n```\n\nPrismedia will:\n- look for options in `nfo.txt`\n- look for options in `samples.txt` (from directory name) and erase any previous conflicting options\n- look for options in `yourvideo1.txt` (from video name) and erase any previous conflicting options\n- look for options in `cli_nfo.txt` (from the `--nfo` in command line) and erase any previous conflicting options\n- erase any previous option regarding CCA as it\'s specified in cli with `--cca`\n- take `yourvideo1.jpg` as thumbnail if no other files has been specified in previous NFO\n\nIn other word, Prismedia will use option given in cli, then look for option in cli_nfo.txt, then complete with video_name.txt, then directory_name.txt, and finally complete with nfo.txt\n\nIt allows to specify more easily default options for an entire set of video, directory, playlist and so on.\n\n## Strict check options\nSince prismedia v0.10.0, a bunch of special options have been added to force the presence of parameters before uploading.\nStrict options allow you to force some option to be present when uploading a video. It\'s useful to be sure you do not\nforget something when uploading a video, for example if you use multiples NFO. You may force the presence of description,\ntags, thumbnail, ...\nAll strict option are optionals and are provided only to avoid errors when uploading :-)\nAll strict options can be specified in NFO directly, the only strict option mandatory on cli is --withNFO\nAll strict options are off by default.\n\nAvailable strict options:\n  - --withNFO         Prevent the upload without a NFO, either specified via cli or found in the directory\n  - --withThumbnail       Prevent the upload without a thumbnail\n  - --withName        Prevent the upload if no name are found\n  - --withDescription     Prevent the upload without description\n  - --withTags        Prevent the upload without tags\n  - --withPlaylist    Prevent the upload if no playlist\n  - --withPublishAt    Prevent the upload if no schedule\n  - --withPlatform    Prevent the upload if at least one platform is not specified\n  - --withCategory    Prevent the upload if no category\n  - --withLanguage    Prevent upload if no language\n  - --withChannel     Prevent upload if no channel\n\n## Features\n\n- [x] Youtube upload\n- [x] Peertube upload\n- Support of videos parameters (description, tags, category, licence, ...)\n  - [x] description\n  - [x] tags (no more than 30 characters per tag as Peertube does not support it)\n  - [x] categories\n  - [x] license: cca or not (Youtube only as Peertube uses Attribution by design)\n  - [x] privacy (between public, unlisted or private)\n  - [x] enabling/disabling comment (Peertube only as Youtube API does not support it)\n  - [x] nsfw (Peertube only as Youtube API does not support it)\n  - [x] set default language\n  - [x] thumbnail\n  - [x] multiple lines description (see [issue 4](https://git.lecygnenoir.info/LecygneNoir/prismedia/issues/4))\n  - [x] add videos to playlist\n  - [x] create playlist\n  - [x] schedule your video with publishAt\n  - [x] combine channel and playlist (Peertube only as channel is Peertube feature). See [issue 40](https://git.lecygnenoir.info/LecygneNoir/prismedia/issues/40) for detailed usage.\n- [x] Use a config file (NFO) file to retrieve videos arguments\n- [x] Allow choosing peertube or youtube upload (to retry a failed upload for example)\n- [x] Usable on Desktop (Linux and/or Windows and/or MacOS)\n- [x] Different schedules on platforms to prepare preview\n- [x] Possibility to force the presence of upload options\n- [ ] Copy and forget, eg possibility to copy video in a directory, and prismedia uploads itself: [Work in progress](https://git.lecygnenoir.info/Zykino/prismedia-autoupload) thanks to @Zykino 🎉 (Discussions in [issue 27](https://git.lecygnenoir.info/LecygneNoir/prismedia/issues/27))  \n- [ ] A usable graphical interface\n\n## Compatibility\n\n - If you still use python2, use the version 0.7.1 (no more updated)\n - If you use peertube before 1.0.0-beta4, use the version inside tag 1.0.0-beta3\n\n## Inspirations\nInspired by [peeror](https://git.rigelk.eu/rigelk/peeror) and [youtube-upload](https://github.com/tokland/youtube-upload)\n\n## Contributors\nThanks to: @LecygneNoir, @Zykino, @meewan, @rigelk 😘',
    'author': 'LecygneNoir',
    'author_email': 'git@lecygnenoir.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.lecygnenoir.info/LecygneNoir/prismedia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
