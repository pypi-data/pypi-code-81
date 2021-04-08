# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord-stubs']

package_data = \
{'': ['*'], 'discord-stubs': ['ext/commands/*', 'ext/tasks/*']}

install_requires = \
['discord.py>=1.7.0,<1.8.0', 'mypy>=0.800', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'discord.py-stubs',
    'version': '1.7.1',
    'description': 'discord.py stubs',
    'long_description': '# discord.py-stubs\n\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/bryanforbes/discord.py-stubs/blob/master/LICENSE)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nThis package contains type stubs to provide more precise static types and type inference for discord.py.\n\n## Installation\n\n```\npip install discord.py-stubs\n```\n\n**NOTE:** Because `discord.py` uses namespace packages for its extensions, `mypy` must be configured to use namespace packages either with the `--namespace-packages` command line flag, or by setting `namespace_packages = True` in your `mypy` configuration file. See the [import discovery](https://mypy.readthedocs.io/en/stable/command_line.html#import-discovery) section of the `mypy` documentation for more details.\n\n## Usage Notes\n\nIn most cases, installing this package will enable developers to type check their discord.py bots using mypy out of the box. However, if developers wish to subclass the classes in `discord.ext.commands` they will need to follow the `mypy` documentation outlining how to use [classes that are generic in stubs but not at runtime](https://mypy.readthedocs.io/en/stable/common_issues.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime):\n\n```python\nfrom typing import TYPE_CHECKING\nfrom discord.ext import commands\n\nclass MyContext(commands.Context):\n    ...\n\nif TYPE_CHECKING:\n    Cog = commands.Cog[MyContext]\nelse:\n    Cog = commands.Cog\n\nclass MyCog(Cog):\n    ...\n```\n\nIn order to avoid this issue, developers can use [`discord-ext-typed-commands`](https://github.com/bryanforbes/discord-ext-typed-commands/):\n\n```python\nfrom discord.ext import typed_commands\n\nclass MyContext(typed_commands.Context):\n    ...\n\nclass MyCog(typed_commands.Cog[MyContext]):\n    ...\n```\n\n## Development\n\nMake sure you have [poetry](https://python-poetry.org/) installed.\n\n```\npoetry install\npoetry run pre-commit install --hook-type pre-commit --hook-type post-checkout\n```\n\n\n## Version numbering scheme\n\nThe **major** and **minor** version numbers of `discord.py-stubs` will match the **major** and **minor** version numbers of the `discord.py` release the stubs represent. For instance, if you are using `discord.py` version `1.7.4`, you would use `discord.py-stubs` version `1.7.X` where `X` is the latest **patch** version of the stubs. Using semver dependency specifications, `discord.py-stubs` version `~1.7` is designed to work with `discord.py` version `~1.7`.\n\nIn addition, `discord.py-stubs` will indicate which versions of the runtime library are compatible through its dependency information (as suggested in PEP-561).\n',
    'author': 'Bryan Forbes',
    'author_email': 'bryan@reigndropsfall.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bryanforbes/discord.py-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
