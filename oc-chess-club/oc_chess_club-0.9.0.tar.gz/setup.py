# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oc_chess_club',
 'oc_chess_club.controller',
 'oc_chess_club.models',
 'oc_chess_club.views']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'colorama>=0.4.4,<0.5.0',
 'shellingham>=1.4.0,<2.0.0',
 'tinydb>=4.4.0,<5.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'oc-chess-club',
    'version': '0.9.0',
    'description': 'CLI to manage tournaments and players for a chess club',
    'long_description': '# oc_chess_club [![GitHub release (latest by date)](https://img.shields.io/github/v/release/pablolec/oc_chess_club)](https://github.com/PabloLec/oc_chess_club/releases/) [![GitHub](https://img.shields.io/github/license/pablolec/oc_chess_club)](https://github.com/PabloLec/oc_chess_club/blob/main/LICENCE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n:books: Made for an [OpenClassrooms](https://openclassrooms.com) studies project.\n\noc_chess_club manages tournaments and players for a chess club.  \nMain dependencies are [typer](https://github.com/tiangolo/typer/) for the CLI part and [TinyDB](https://github.com/msiemens/tinydb) for the lightweight database.\n\nYou will need **Python 3.9+** as the project type hints generics from standard collections. (See [PEP 585](https://www.python.org/dev/peps/pep-0585/))\n\n---\n\n<img class="emoji" title=":fr:" alt=":fr:" src="https://github.githubassets.com/images/icons/emoji/unicode/1f1eb-1f1f7.png" data-canonical-src="https://github.githubassets.com/images/icons/emoji/unicode/1f1eb-1f1f7.png" width="20" height="20" align="absmiddle"> **Have a look at the [documentation](https://pablolec.github.io/oc_chess_club)** <img class="emoji" title=":fr:" alt=":fr:" src="https://github.githubassets.com/images/icons/emoji/unicode/1f1eb-1f1f7.png" data-canonical-src="https://github.githubassets.com/images/icons/emoji/unicode/1f1eb-1f1f7.png" width="20" height="20" align="absmiddle">\n\n---\n\n## Installation\n\n```console\npython3 -m pip install oc_chess_club\n```\n\n## Usage\n\nTo start the CLI, simply type:\n\n```console\npython3 -m oc_chess_club\n```\n\nTo learn more, please refer to the [documentation](https://pablolec.github.io/oc_chess_club) (:fr:).\n\n## Improvement\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PabloLec/oc_chess_club',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
