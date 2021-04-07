# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kak_plugins', 'kak_plugins.apis']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['github-permalink = kak_plugins.github_permalink:main']}

setup_kwargs = {
    'name': 'kak-plugins',
    'version': '0.4.0',
    'description': '',
    'long_description': '[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)\n[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)\n\n\n# kak_plugins\nZach\'s plugins for the [Kakoune](http://kakoune.org/) text editor.\n\n## Installation\nI recommend using [pipx](https://pipxproject.github.io/pipx/installation/) for installation. It allows you to install python packages on your machine in separate virtual environments without having to manage the virtual environments yourself. `pip` also works if you prefer that.\n```\npipx install kak_plugins\n```\n\n## Dependencies\n* [Kakoune](http://kakoune.org/) of course\n* [kakoune.cr](https://github.com/alexherbo2/kakoune.cr)\n    * enables us to retrieve info from Kakoune\n    * provides an interface to control Kakoune\n* A clipboard command-line utility. I use these:\n    * `pbcopy` for OSX\n    * [xclip](https://github.com/astrand/xclip) for Linux\n    * [wl-clipboard](https://github.com/bugaevc/wl-clipboard) for Wayland (if you don\'t know what this is and you use Linux, you\'ll probably use `xclip`)\n## Setup\nThere are some environment varibles you will need to define in order to use these plugins. You would probably define these in your `~/.bashrc`, `zshrc`, or `~/.profile`. I define mine [here](https://github.com/abstractlyZach/dotfiles/blob/master/common/.profile]\n```\n# program that reads stdin and writes to your system clipboard\nexport CLIPBOARD="pbcopy"\n```\n\n## Logging\nLogs are a good way of getting an idea of what\'s going on in the code. Logs will be written in a temporary directory in a file that has the name of the plugin. See here for rules on [where you can find logs on your system](https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir)\n\n# Plugins\n\n## github-permalink\nCreate a permalink to a line or range of lines in a GitHub repo that matches your current selection in Kakoune. Then copy that permalink to your clipboard program.\n1. open a file in Kakoune\n1. make a selection\n1. in normal mode, type `:$ github-permalink`\n1. you now have a permalink to your kakoune selection. it should look something like this https://github.com/abstractlyZach/kak_plugins/blob/write-readme/README.md#L40\n\nI like [binding this command](https://github.com/abstractlyZach/dotfiles/blob/master/kak/kakrc#L12) to hotkeys so I can hit 2 buttons and then paste the link into Slack or something.\n',
    'author': 'abstractlyZach',
    'author_email': 'zach3lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abstractlyZach/kak_plugins',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
