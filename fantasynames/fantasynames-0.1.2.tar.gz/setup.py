# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fantasynames', 'fantasynames.tests']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'flake8>=3.9.0,<4.0.0',
 'mypy>=0.812,<0.813',
 'pytest>=6.2.3,<7.0.0']

setup_kwargs = {
    'name': 'fantasynames',
    'version': '0.1.2',
    'description': 'A fantasy themed random name generator.',
    'long_description': '# Fantasy Name Generator\n\n[![PyPI version](https://badge.fury.io/py/fantasynames.svg)](https://badge.fury.io/py/fantasynames)\n\nA random name generator that produces names aligning (more or less) with common conventions for fantasy characters in fictional media such as Dungeons and Dragons or World of Warcraft.\n\n## Installation\n\n`python3 -m pip install fantasynames`\n\nOr if your project is using Poetry:\n\n`poetry add fantasynames`\n\n## Usage\n\nThe following name generating methods are provided for a variety of different stereotypical fantasy "races", as well as a few different "medieval-y" languages:\n\n```python\nimport fantasynames as names\n\nnames.elf()\n# Example outputs: \'Farathia Eaviel\', \'Iethian Willowblossom\'\n\nnames.dwarf()\n# Example outputs: \'Dagdr Steelbeard\', \'Thorinna Ironstrike\'\n\nnames.hobbit()\n# Example outputs: \'Libby Honeyfoot\', \'Flublius Sweetscone\'\n\nnames.french()\n# Example outputs: \'Richert Roublac\', \'Clavena de Clardalle\'\n\nnames.anglo()\n# Example outputs: \'Brandin of Avonlyn\', \'Kallem Davenmere\'\n\nnames.human()\n# Example outputs: \'Danric du Tourbloc\', \'Sumia Sageholme\'\n```\n\nNote that `human()` provides a diverse mix of different first and last name styles, including `anglo()` and `french()`...and more!\n\nYou can also pass a string argument to specify whether you want to recieve masculine or feminine names. By default, it\'s totally random:\n\n```python\nnames.human() # this will randomly generate either a male or female name\n\nnames.human(\'any\') # this is equivalent to the above, in case you want to be specific\n\nnames.human(\'male\') # this will generate a masculine name\n\nnames.human(\'female\') # this will generate a feminine name\n```\n\n## Contributing\n\n### Poetry\n\nThis package uses [Poetry](https://python-poetry.org/) for package management. After checking out the repo, use `poetry install` to install all the required dependencies. Anytime you need to add a package, use:\n\n```\npoetry add PACKAGE_NAME_HERE\n```\n\n### Linting / Formatting\n\nWe do code formatting with [Python Black](https://github.com/psf/black), additional linting with [flake8](https://flake8.pycqa.org/en/latest/manpage.html), and type checking with [mypy](http://mypy-lang.org/). Before opening a PR, please make sure to run all of these. Below is a helpful command to do them all at once:\n\n```\npoetry run black fantasynames && poetry run flake8 fantasynames && poetry run mypy fantasynames\n```\n\n### Guides\n\nIf you want to make your own name generators, check out:\n- [How to Add a New Name Generator Guide](docs/new-generator-guide.md)\n\nAnd then if you want to ramp up the complexity, take a look at:\n- [Transformation Guide](docs/transformation-guide.md)\n',
    'author': 'Jessica Peck',
    'author_email': 'jessypeck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jessypeck/fantasynames',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
