# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preserve', 'preserve.connectors']

package_data = \
{'': ['*']}

install_requires = \
['halo>=0.0.30,<0.0.31',
 'pydantic>=1.6.1,<2.0.0',
 'pymongo>=3.11.0,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10.1,<0.11.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['preserve = preserve.cli:app']}

setup_kwargs = {
    'name': 'preserve',
    'version': '0.1.2a0',
    'description': 'A simple key/value store with multiple backends.',
    'long_description': '# 🥫 Preserve - A simple Python Key/Value database with multiple backends.\n\n> ⚠️ Preserve is alpha software and currently in development (i.e., no tests).\n\nPreserve is a simple (simplistic) key/value store for storing JSON-like data in different backends. Its API is based on the standard Python dictionary API.\n\n\n## ℹ️ Installation and Usage\nPreserve can be installed using pip:\n```\npip install preserve\n```\n\nPreserve can be also installed from Github directly using the following command:\n```\npip install git+https://github.com/evhart/preserve#egg=preserve\n```\n\n### 📒 Requirements\nPreserve needs the following libraries installed and Python 3.6+ (tested on Python 3.8):\n* [halo](https://github.com/manrajgrover/halo)\n* [pydantic](https://pydantic-docs.helpmanual.io/)\n* [pymongo](https://pymongo.readthedocs.io/)\n* [tabulate](https://github.com/astanin/python-tabulate)\n* [typer](https://typer.tiangolo.com/)\n\n### 🐍 Python API\n\nIf you know how to use Python dictionaries, you already know how to use preserve. Simply use the backend connector that corresponds to your database and you are ready to go.\n\nYou can either create a new database from a standarised database URI or using the driver parameters:\n\n```python\nimport preserve\n\n# Using parameters:\njam_db1 = preserve.open(\'shelf\', filename="preserve.dbm")\njam_db1[\'strawberry\'] = {\'name\': \'Strawbery Jam\', \'ingredients\': [\'strawberry\', \'sugar\']}\n\n\n# Using URI:\njam_db2 = preserve.from_uri("mongodb://127.0.0.1:27017/preserves?collection=jam")\njam_db2[\'currant\'] = {\'name\': \'Currant Jam\', \'ingredients\': [\'currant\', \'sugar\']}\n\n```\n\n### 🖥️ Command Line Interface (CLI)\nPreserve has a simple CLI utility that can be access using the ```preserve``` command. Preserve support migrating/exporting data from one database ot another database and showing the firs rows from databases.\n\n```\nUsage: preserve [OPTIONS] COMMAND [ARGS]...\n\n  🥫 Preserve - A simple Key/Value database with multiple backends.\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  connectors  List available connectors.\n  export      Export a database to a different output.\n  header      Get header of a given database table.\n```\n',
    'author': 'Grégoire Burel',
    'author_email': 'evhart@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evhart/preserve/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
