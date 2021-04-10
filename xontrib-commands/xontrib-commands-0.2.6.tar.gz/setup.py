# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib', 'xontrib.commands']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "4.0"': ['arger>=1.2.7,<2.0.0',
                                                         'rich']}

setup_kwargs = {
    'name': 'xontrib-commands',
    'version': '0.2.6',
    'description': 'Useful xonsh-shell commands/alias functions',
    'long_description': '<p align="center">\nUseful xonsh-shell commands/alias/completer functions\n</p>\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-commands\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-commands\n```\n\n## Usage\n\n``` bash\nxontrib load commands\n```\n\n## building alias\n\nUse [`xontrib.commands.Command`](https://github.com/jnoortheen/xontrib-commands/blob/main/xontrib/commands.py#L9) \nto build [arger](https://github.com/jnoortheen/arger) dispatcher\nfor your functions.\n\n```py\nfrom xontrib.commands import Command\n@Command.reg\ndef record_stats(pkg_name=".", path=".local/stats.txt"):\n    stat = $(scc @(pkg_name))\n    echo @($(date) + stat) | tee -a @(path)\n```\n\nNow a full CLI is ready\n```sh\n$ record-stats --help                                                                        \nusage: xonsh [-h] [-p PKG_NAME] [-a PATH]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PKG_NAME, --pkg-name PKG_NAME\n  -a PATH, --path PATH\n```\n\n## Commands\n\n- each of the commands use argparser. Please use `cmd --help` to get more info and usage examples.\n\n### 1. reload-mods\n![](./docs/2020-12-02-14-30-47.png)\n\n### 2. report-key-bindggs\n![](./docs/2020-12-02-14-30-17.png)\n\n### 3. dev\n- command to cd around fast. \n- much like https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/pj\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-commands',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
