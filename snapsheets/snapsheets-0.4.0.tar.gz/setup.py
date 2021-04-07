# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'icecream>=2.1.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.4.0',
    'description': 'Wget snapshots of google sheets',
    'long_description': "![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nWget snapshots of Google Spreadsheets\n\nThis package enables to wget Google Spreadsheets without login.\n(Spreadsheets should be shared with public link)\n\n\n---\n\n# Usage\n\n```python\n>>> import snapsheets as ss\n>>> ss.add_config('test_config.yml')\n>>> ss.get('test1', by='wget')\n```\n\n---\n\n## Configuration\n\n- Make your config files in ``./config/``\n\n\n```yaml\nvolumes:\n  snapd: 'snapd/'\n  logd: 'varlogs/'\n\noptions:\n  wget:\n    '--quiet'\n\ndatefmt:\n  '%Y%m%dT%H%M%S'\n\nsheets:\n  test1:\n    key: '1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM'\n    gid: 'None'\n    format: 'xlsx'\n    sheet_name:\n      - 'シート1'\n      - 'シート2'\n    stem: 'test_sheet'\n    datefmt: '%Y'\n```\n\n## ``volumes``\n\n- directories to save data\n\n## ``options``\n\n- set options for ``wget``\n\n## ``datefmt``\n\n- set prefix to saved spreadsheet\n\n## ``sheet``\n\n- google spreadsheet info\n\n\n---\n\n# Documents\n\n- https://shotakaha.gitlab.io/snapsheets/\n\n---\n\n# Stats\n\n![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)\n",
    'author': 'shotakaha',
    'author_email': 'shotakaha+py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://shotakaha.gitlab.io/snapsheets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
