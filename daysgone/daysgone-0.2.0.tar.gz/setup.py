# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daysgone']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'rich>=10.1.0,<11.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['daysgone = daysgone.main:app']}

setup_kwargs = {
    'name': 'daysgone',
    'version': '0.2.0',
    'description': '',
    'long_description': '# `daysgone`\n\nThis is a cli that outputs dates.\n\n**Usage**:\n\n```console\n$ daysgone [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `adddays`: Add number of days and date to get the number...\n* `daterange`: Enter a start date and end date to get a list...\n* `daysago`: Enther the number of days you want to go back...\n* `daysfromnow`: Enter the number of days to get the date.\n* `diff`: Calculates difference in days between two...\n* `isweekday`: Find out if the date is a weekend or date.\n* `isweekend`: Check if given date is a weekend.\n\n## `daysgone adddays`\n\nAdd number of days and date to get the number of days.\n\nIf no date is given, then todays date will be used.\n\n**Usage**:\n\n```console\n$ daysgone adddays [OPTIONS] DAYS\n```\n\n**Arguments**:\n\n* `DAYS`: Number of days from date given.  [required]\n\n**Options**:\n\n* `-d, --date TEXT`: Enter date in this format: MM-DD-YYYY\n* `--help`: Show this message and exit.\n\n## `daysgone daterange`\n\nEnter a start date and end date to get a list of dates between.\n\n**Usage**:\n\n```console\n$ daysgone daterange [OPTIONS] START END\n```\n\n**Arguments**:\n\n* `START`: Enter the start date  [required]\n* `END`: Enter the end date  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daysgone daysago`\n\nEnther the number of days you want to go back to.\n\n**Usage**:\n\n```console\n$ daysgone daysago [OPTIONS] DAYS\n```\n\n**Arguments**:\n\n* `DAYS`: Number of days you want to go back to.  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daysgone daysfromnow`\n\nEnter the number of days to get the date.\n\n**Usage**:\n\n```console\n$ daysgone daysfromnow [OPTIONS] DAYS\n```\n\n**Arguments**:\n\n* `DAYS`: Get day from number of days given.  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daysgone diff`\n\nCalculates difference in days between two dates.\n\n**Usage**:\n\n```console\n$ daysgone diff [OPTIONS] START END\n```\n\n**Arguments**:\n\n* `START`: Start date. Format: MM-DD-YYYY  [required]\n* `END`: End date. Format: MM-DD-YYYY  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daysgone isweekday`\n\nFind out if the date is a weekend or date.\n\n**Usage**:\n\n```console\n$ daysgone isweekday [OPTIONS] DATE\n```\n\n**Arguments**:\n\n* `DATE`: Enter date in this format: MM-DD-YYYY  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daysgone isweekend`\n\nCheck if given date is a weekend.\n\n**Usage**:\n\n```console\n$ daysgone isweekend [OPTIONS] DATE\n```\n\n**Arguments**:\n\n* `DATE`: Enter date in this format: MM-DD-YYYY  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'Mr.Nobody',
    'author_email': 'mrcartoonster@yahoo.com',
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
