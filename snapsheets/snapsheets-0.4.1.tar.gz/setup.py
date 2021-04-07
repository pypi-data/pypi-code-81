# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'docopt>=0.6.2,<0.7.0',
 'icecream>=2.1.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.4.1',
    'description': 'Wget snapshots of google sheets',
    'long_description': '![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nWget snapshots of Google Spreadsheets\n\nThis package enables to wget Google Spreadsheets without login.\n(Spreadsheets should be shared with public link)\n\n\n---\n\n# Usage\n\n```python\n>>> import snapsheets as ss\n>>> sample_url1 = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n>>> sheet = ss.Sheet(url=sample_url1, saved=".", desc="Get Sample Sheet")\n>>> sheet.snapshot()\n📣 Get Sample Sheet\n🤖 Downloaded snapshot.xlsx\n🚀 Renamed to 20210407T172202_snapshot.xlsx\n```\n\n---\n\n## Usage with configuration files\n\nTBA\n\n---\n\n\n# v0.2.3 or older\n\n- Added DeprecationWarnings\n- It still works\n\n```python\n>>> print("💥💥💥 deprecated since version 0.2.3 💥💥💥")\n>>> fname = "config/config.yml"\n>>> ss.config.add_config(fname)\nsnapsheets/sandbox/snapper.py:28: DeprecationWarning: Call to deprecated function (or staticmethod) add_config. (Will be removed.) -- Deprecated since version 0.2.3.\n  ss.config.add_config(fname)\n>>> fname = "config/gsheet.yml"\n>>> ss.config.add_config(fname)\nsnapsheets/sandbox/snapper.py:30: DeprecationWarning: Call to deprecated function (or staticmethod) add_config. (Will be removed.) -- Deprecated since version 0.2.3.\n  ss.config.add_config(fname)\n>>> fname = ss.gsheet.get("test1", by="wget")\nsnapsheets/sandbox/snapper.py:31: DeprecationWarning: Call to deprecated function (or staticmethod) get. (Will be removed) -- Deprecated since version 0.3.0.\n  fname = ss.gsheet.get("test1", by="wget")\n2021-04-07 19:44:18 - INFO - gsheet.py - snapsheets.gsheet - download - ダウンロードするよ : test1\n2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - download - ダウンロードしたよ : snapd/test_sheet.xlsx\n2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - backup - 移動するよ : test_sheet.xlsx\n2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - backup - 移動したよ : 2021_test_sheet.xlsx\n```\n\n---\n\n\n# Documents\n\n- https://shotakaha.gitlab.io/snapsheets/\n\n---\n\n# PyPI package\n\n- https://pypi.org/project/snapsheets/\n\n![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)\n',
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
