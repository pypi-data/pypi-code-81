# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['realm',
 'realm.cli',
 'realm.cli.commands',
 'realm.cli.core',
 'realm.entities',
 'realm.utils',
 'realm.utils.filters']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'colorama>=0.4.4,<0.5.0', 'toml>=0.10.2,<0.11.0']

extras_require = \
{'tasks': ['poethepoet>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['realm = realm.cli.application:cli']}

setup_kwargs = {
    'name': 'realm',
    'version': '0.1.0rc0',
    'description': 'A tool for managing python poetry projects',
    'long_description': '## Realm\nRealm is tool for managing multiple poetry projects in the same git repository.\n\nThis project is inspired by the `lerna` project available for JavaScript\n\n[![Build Status](https://github.com/orlevii/realm/workflows/build/badge.svg?branch=master&event=push)](https://github.com/orlevii/realm/actions/workflows/build.yml?query=branch%3Amaster)\n\n### Requirements\nIn order to start using realm, you first need to have [poetry](https://github.com/python-poetry/poetry) installed\n\n### Commands\n* <code>realm init</code> - Initializes a new realm repo\n* <code>realm install</code> - Executes `poetry install` on all projects\n* <code>realm ls</code> - Prints all projects managed\n* <code>realm run</code> - Executes a command on all projects\n* <code>realm task</code> - Runs a poe task on all projects containing this task (requires poethepoet)\n\n#### Filtering\nYou can set up filters to affect only certain projects\n\nFor example, you can install only changed projects \n```bash\n$ realm install --since origin/master\n```\n\nAvailable filters:\n* <code>--since</code> - Includes only projects changed since the specified ref\n* <code>--scope</code> - Includes only projects that match the given pattern\n* <code>--ignore</code> - Filters out projects that match the given pattern\n* <code>--match</code> - Filters by a field specified in `pyproject.toml`\n',
    'author': 'Or Levi',
    'author_email': 'orlevi128@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orlevii/realm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
