# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_reconcile_levenshtein']

package_data = \
{'': ['*']}

install_requires = \
['csv-reconcile>=0.2.1,<0.3.0', 'python-Levenshtein>=0.12.2,<0.13.0']

entry_points = \
{'csv_reconcile.scorers': ['levenshtein = csv_reconcile_levenshtein']}

setup_kwargs = {
    'name': 'csv-reconcile-levenshtein',
    'version': '0.1.2',
    'description': 'Levenshtein distance scoring plugin for csv-reconcile',
    'long_description': '\n# Table of Contents\n\n1.  [CSV Reconcile Levenshtein distance scoring plugin](#orgaad35af)\n\n\n<a id="orgaad35af"></a>\n\n# CSV Reconcile Levenshtein distance scoring plugin\n\nA scoring plugin for [csv-reconcile](https://github.com/gitonthescene/csv-reconcile) using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  See csv-reconcile for details.\n\n',
    'author': 'Douglas Mennella',
    'author_email': 'trx2358-pypi@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gitonthescene/csv-reconcile-levenshtein',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
