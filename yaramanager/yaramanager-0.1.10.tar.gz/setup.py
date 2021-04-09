# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaramanager',
 'yaramanager.commands',
 'yaramanager.db',
 'yaramanager.models',
 'yaramanager.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.2,<2.0.0',
 'alembic>=1.5.8,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'plyara>=2.1.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.0.0,<11.0.0',
 'toml>=0.10.2,<0.11.0',
 'yara-python>=4.0.5,<5.0.0',
 'yarabuilder>=0.0.5,<0.0.6']

entry_points = \
{'console_scripts': ['yaramanager = yaramanager.commands.cli:cli',
                     'ym = yaramanager.commands.cli:cli']}

setup_kwargs = {
    'name': 'yaramanager',
    'version': '0.1.10',
    'description': 'CLI tool to manage your yara rules',
    'long_description': '<div align="center">\n\n![License:MIT](https://img.shields.io/github/license/3c7/yaramanager?style=flat-square&color=blue) \n![Version](https://img.shields.io/pypi/v/yaramanager?style=flat-square&color=blue)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/yaramanager?color=blue&style=flat-square)\n[![Awesome Yara](https://img.shields.io/static/v1?label=awesome&message=yara&style=flat-square&color=ff69b4&logo=awesome-lists)](https://github.com/InQuest/awesome-yara)\n\n</div>\n\n# Yara Manager\nA simple program to manage your yara ruleset in a (sqlite) database.\n\n## Todos\n- [ ] Implement backup and sharing possibilities\n\n## Installation\nInstall it using pip:\n```shell\npip install yaramanager\n```\nOr grab one of the prebuilt binaries from the release page.\n\n## Configuration\nYara Manager creates a fresh config if none exists. If you update from an older version, please pay attention to freshly\nadded [config options](resources/config.toml). You can reset you configuration using `ym config reset`, however, this\nwill also overwrite any custom changes you made.  \n\n```toml\n## Editor\n# editor contains the command used to start the editor. Note that this must be a list of the command and the needed\n# parameters, e.g. `editor = ["codium", "-w"]`.\neditor = [ "codium", "-w" ]\n```\nThe most important configuration to change is probably your editor. The default configuration uses `codium -w` for \nopening rules. You can use e.g. `EDITOR=vim DISABLE_STATUS=1 ym config edit` to open you config in Vim (and you can type\n`:wq` to save your changes and quit :P). After changing the editor path, you are good to go! The following asciinema\nshows how to quickly overwrite the editor set in the config:\n\n[![Asciinema: Temporarily overwrite the used editor.](https://asciinema.org/a/auX5tjpeUiHCnsfCrO0MEPRY9.svg)](https://asciinema.org/a/auX5tjpeUiHCnsfCrO0MEPRY9)\n\n```toml\n# Databases\n# A list of databases. Every database needs to define a driver and a path, such as\n#\n# [[yaramanager.db.databases]]\n# driver = "sqlite"\n# path = "/home/user/.config/yaramanager/data.db"\n[[yaramanager.db.databases]]\ndriver = "sqlite"\npath = "/home/3c7/.config/yaramanager/myrules.db"\n```\nIf you want to use multiple databases (which is pretty useful if you use rules from different sources or with different \nclassifications), you can add them to the config file, too.\n\n## Features\n### General usage\n```\n$ ym\nUsage: ym [OPTIONS] COMMAND [ARGS]...\n\n  ym - yaramanager. Use the commands shown below to manage your yara\n  ruleset. By default, the manager uses codium as editor. You can change\n  that in the config file or using EDITOR environment variable. When using\n  editors in the console, you might want to disable the status display using\n  DISABLE_STATUS.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  add      Add a new rule to the database.\n  config   Review and change yaramanager configuration.\n  db       Manage your databases\n  del      Delete a rule by its ID or name.\n  edit     Edits a rule with your default editor.\n  export   Export rules from the database.\n  get      Get rules from the database.\n  help     Displays help about commands\n  list     Lists rules available in DB.\n  new      Create a new rule using you preferred editor.\n  parse    Parses rule files.\n  read     Read rules from stdin.\n  ruleset  Manage your rulesets\n  scan     Scan files using your rulesets.\n  search   Searches through your rules.\n  stats    Prints stats about the database contents.\n  tags     Show tags and the number of tagged rules\n  version  Displays the current version.\n```\n\n### Yara Manager Showcase\n[![Asciiname: Yara Manager showcase](https://asciinema.org/a/8QbXQoBEeJIwVcf2mWqiRTNBj.svg)](https://asciinema.org/a/8QbXQoBEeJIwVcf2mWqiRTNBj)\n',
    'author': '3c7',
    'author_email': '3c7@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/3c7/yaramanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
