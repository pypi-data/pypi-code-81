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
    'version': '0.5.0',
    'description': '',
    'long_description': '[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)\n[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)\n\n\n# Zach\'s Overengineered Kakoune Plugins\nThey say that for any given job, if [Python](https://www.python.org/) isn\'t the best tool for the job, then it\'s the second-best tool for the job.\n\n[Kakoune](http://kakoune.org/) has a lot of amazing plugins and user-modes, and they\'re usually not written in Python.\n\nSo, since I must be working with the second-best tool for the job, I thought I would go the whole 9 yards and overengineer the h*ck out of it 😉. In true [abstractlyZach](https://www.github.com/abstractlyZach) fashion, this project includes:\n- reimplementations of awesome scripts that could be one-liners in `bash` with, like, 5 pipes\n- [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)\n- readability as a priority\n- [composition over inheritance](https://realpython.com/inheritance-composition-python/)\n- rigorous testing\n- helpful command-line menus\n- milliseconds of extra run-time! Python is an interpreted language!\n- intense CI practices\n- linting and autoformatting\n- lots of documentation\n- [minimal use of Mocks](https://www.youtube.com/watch?v=rk-f3B-eMkI), maximal use of better test doubles like Fakes and Stubs\n- robust error-handling\n- fine-grained logging options\n\nAlso, I was pretty excited about [kakoune.cr](https://github.com/alexherbo2/kakoune.cr), but I was super fuzzy on how to actually use it. Hopefully these plugins will serve as living documentation on some good ways to leverage this tool.\n\n## Installation\nI recommend using [pipx](https://pipxproject.github.io/pipx/installation/) for installation. It allows you to install python packages on your machine in separate virtual environments without having to manage the virtual environments yourself. `pip` also works if you prefer that.\n```\npipx install kak_plugins\n```\n\n## Dependencies\n* [Kakoune](http://kakoune.org/), of course 😄\n* [kakoune.cr](https://github.com/alexherbo2/kakoune.cr)\n    * enables us to retrieve info from Kakoune\n    * provides an interface to control Kakoune\n* A clipboard command-line utility. I use these:\n    * `pbcopy` for OSX\n    * [xclip](https://github.com/astrand/xclip) for Linux\n    * [wl-clipboard](https://github.com/bugaevc/wl-clipboard) for Wayland (if you don\'t know what this is and you use Linux, you\'ll probably use `xclip`)\n\n\n## Setup\nThere are some environment varibles you will need to define in order to use these plugins. You would probably define these in your `~/.bashrc`, `zshrc`, or `~/.profile`. I define mine [here](https://github.com/abstractlyZach/dotfiles/blob/master/common/.profile)\n```\n# program that reads stdin and writes to your system clipboard\nexport CLIPBOARD="pbcopy"\n```\n\n# Plugins\n\n## github-permalink\nCreate a permalink to a file on GitHub with lines pre-selected. [Example](https://github.com/abstractlyZach/kak_plugins/blob/main/src/kak_plugins/github_permalink.py#L26-L53). The selected line or range of lines matches your current selection in Kakoune and will be copied to your clipboard program.\n```\ngithub-permalink --help\n```\n\n### in kak\nThis method is great for using in your everyday editing\n\n1. open a file in Kakoune\n1. make a selection\n1. in normal mode, use `:$ github-permalink`\n1. you now have a permalink to your kakoune selection. it should look something like this https://github.com/abstractlyZach/kak_plugins/blob/write-readme/README.md#L40\n\nI like [binding this command](https://github.com/abstractlyZach/dotfiles/blob/master/kak/kakrc#L12) to hotkeys so I can hit 2 buttons and then paste the link into Slack or something.\n\n### in a terminal\nThis method is great for learning, development, and debugging\n\n1. open a file in kakoune\n1. make a selection\n1. open a connected terminal. there are a couple of recommended methods\n    * use `:>` in normal mode\n    * [kcr-fzf-shell](https://github.com/alexherbo2/kakoune.cr/blob/master/share/kcr/commands/fzf/kcr-fzf-shell)\n1. `github-permalink --help`\n',
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
