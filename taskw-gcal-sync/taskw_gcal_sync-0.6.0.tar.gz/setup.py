# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskw_gcal_sync', 'taskw_gcal_sync.scripts']

package_data = \
{'': ['*'], 'taskw_gcal_sync': ['res/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'bidict>=0.21.2,<0.22.0',
 'click>=7.1.2,<8.0.0',
 'colorlog>=4.8.0,<5.0.0',
 'google-api-python-client>=2.1.0,<3.0.0',
 'google-auth-oauthlib>=0.4.4,<0.5.0',
 'loguru>=0.5.3,<0.6.0',
 'overrides>=3.1.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2021.1,<2022.0',
 'rfc3339>=6.2,<7.0',
 'sh>=1.14.1,<2.0.0',
 'taskw>=1.3.0,<2.0.0',
 'typing>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['tw_gcal_sync = '
                     'taskw_gcal_sync.scripts.tw_gcal_sync:main']}

setup_kwargs = {
    'name': 'taskw-gcal-sync',
    'version': '0.6.0',
    'description': 'Taskwarrior <-> Google Calendar synchronisation tool',
    'long_description': '# Taskwarrior - Google Calendar synchroniser\n\n<table>\n  <td>master</td>\n  <td>\n    <a href="https://github.com/bergercookie/taskw_gcal_sync/actions" alt="master">\n    <img src="https://github.com/bergercookie/taskw_gcal_sync/actions/workflows/ci.yml/badge.svg" /></a>\n  </td>\n  <td>devel</td>\n  <td>\n    <a href="https://github.com/bergercookie/taskw_gcal_sync/actions" alt="devel">\n    <img src="https://github.com/bergercookie/taskw_gcal_sync/actions/workflows/ci.yml/badge.svg?branch=devel" /></a>\n  </td>\n</table>\n\n<a href="https://www.codacy.com/app/bergercookie/taskw_gcal_sync" alt="Quality - devel">\n<img src="https://api.codacy.com/project/badge/Grade/57206a822c41420bb5792b2cb70f06b5"/></a>\n<a href="https://www.codacy.com/app/bergercookie/taskw_gcal_sync">\n<img src="https://api.codacy.com/project/badge/Coverage/57206a822c41420bb5792b2cb70f06b5"/></a>\n<a href=https://github.com/bergercookie/taskw_gcal_sync/blob/devel/LICENSE" alt="LICENCE">\n<img src="https://img.shields.io/github/license/bergercookie/taskw_gcal_sync.svg" /></a>\n<a href="https://pypi.org/project/taskw-gcal-sync/" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/taskw_gcal_sync.svg" /></a>\n<a href="https://badge.fury.io/py/taskw-gcal-sync">\n<img src="https://badge.fury.io/py/taskw-gcal-sync.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/taskw-gcal-sync">\n<img alt="Downloads" src="https://pepy.tech/badge/taskw-gcal-sync"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n```\n _            _                                _\n| |_ __ _ ___| | ____      __   __ _  ___ __ _| |    ___ _   _ _ __   ___\n| __/ _` / __| |/ /\\ \\ /\\ / /  / _` |/ __/ _` | |   / __| | | | \'_ \\ / __|\n| || (_| \\__ \\   <  \\ V  V /  | (_| | (_| (_| | |   \\__ \\ |_| | | | | (__\n \\__\\__,_|___/_|\\_\\  \\_/\\_/____\\__, |\\___\\__,_|_|___|___/\\__, |_| |_|\\___|\n                         |_____|___/           |_____|   |___/\n```\n\n## Description\n\n`taskw_gcal_sync` provides a solution for bidirectional synchronisation between\n[Taskwarrior](https://taskwarrior.org) and [Google\nCalendar](https://calendar.google.com). Given a _Calendar_ name for Google\nCalendar and a _filter_ for Taskwarrior (currently only a single tag is\nsupported and tested) synchronise all the events between them.\n\nOverall, it supports synchronisation on the following events:\n\n- Creation of an event\n- Modification of an (existing) event\n- Deletion of an event\n\nThe aforementioned features should work bidirectional, meaning a reminder\ncreated, modified, or deleted from Google Calendar should also be created,\nmodified, or deleted respectively in TaskWarrior and vice-versa\n\n## Demo - first run - populating calendar in GCal\n\n![demo_gif](https://github.com/bergercookie/taskw_gcal_sync/blob/master/misc/demo.gif)\n\n## Motivation\n\nWhile Taskwarrior is an excellent tool when it comes to keeping TODO lists,\nkeeping track of project goals etc., lacks the portability, simplicity and\nminimalistic design of Google Calendar. The latter also has the following\nadvantages:\n\n- Automatic sync across all your devices\n- Comfortable addition/modification of events using voice commands\n- Actual reminding of events with a variety of mechanisms\n\n## Installation instructions\n\nRequirements:\n\n- Taskwarrior - [Installation instructions](https://taskwarrior.org/download/) -\n  Tested with 2.5.1\n- Python version >= 3.6 (yeah kind of restrictive, but\n  [mypy](http://mypy-lang.org/) rocks!)\n\nInstallation Options:\n\n- Pypi (will not contain latest version): `pip3 install --user --upgrade taskw_gcal_sync`\n- Github: `pip3 install --user git+https://github.com/bergercookie/taskw_gcal_sync`\n- Download and install devel branch locally - bleeding edge\n\n  ```sh\n  git clone https://github.com/bergercookie/taskw_gcal_sync\n  cd taskw_gcal_sync\n  git checkout devel\n  pip3 install --user --upgrade .\n  ```\n\n- Setup using [poetry](https://python-poetry.org/) - handy for local\n  development:\n\n  ```sh\n  git clone https://github.com/bergercookie/taskw_gcal_sync\n  poetry install\n  # get an interactive shell\n  poetry shell\n\n  # now tw_gcal_sync is in your PATH in this shell and you can also edit and the\n  # changes will take instant effect\n  ...\n  ```\n\n## Usage instructions\n\nRun the `tw_gcal_sync` to synchronise the Google calendar of your choice with\nthe selected Taskwarrior tag(s). Run with `--help` for the list of options.\n\n```sh\n# Sync the +remindme Taskwarrior tag with the calendar named "TW Reminders"\n\ntw_gcal_sync --help\ntw_gcal_sync -t remindme -c "TW Reminders"\n```\n\n## Mechanics\n\nTo achieve synchronization across the two services, we use a push-pull mechanism\nwhich is far easier and less troublesome than an automatic synchronization\nsolution. In case the latter behavior is desired, users may just run the\nscript periodically e.g., using cron:\n\n```sh\n$ crontab -e\n...\n\n# Add the following to sync every 10\' - modify Calendar and Tag name accordingly\n# See output and potential errors in your system logs (e.g., `/var/log/syslog`)\n*/10 * * * * tw_gcal_sync -c "TW Reminders" -t "remindme"\n\n```\n\n## Troubleshooting\n\n- Having trouble installing or using the tool? Take a look at either the\n  continuous-integration configuration or the unittsests for the installation\n  steps or the recommended way of using the python code respectively.\n- Something doesn\'t work? Does the script fail midway through?\n\n  - Record the problem and report it in the ISSUES page. Include as much\n    information as possible so that I can reproduce it.\n  - Clean the configuration file. By default that\'s going to be\n    `$HOME/.config/taskw_gcal_sync`\n\n    `rm -rf ~/.config/taskw_gcal_sync`\n\n  - Remove the corresponding Google Calendar\n  - Rerun synchronisation from scratch\n\n## Self Promotion\n\nIf you find this tool useful, please [star it on\nGithub](https://github.com/bergercookie/taskw_gcal_sync)\n\n## TODO List\n\nSee [ISSUES list](https://github.com/bergercookie/taskw_gcal_sync/issues) for\nthe things that I\'m currently either working on or interested in implementing in\nthe near future. In case there\'s something you are interesting in working on,\ndon\'t hesitate to either ask for clarifications or just do it and directly make\na PR.\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/taskw_gcal_sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
