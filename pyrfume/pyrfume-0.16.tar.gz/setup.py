# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrfume', 'pyrfume.loaders', 'pyrfume.unit_test']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0',
 'dask[bag]>=2.17.0,<3.0.0',
 'datajoint>=0.12.6b1',
 'deap>=1.3.1',
 'eden-kernel>=0.3.1335',
 'flake8>=3.8.2',
 'ipython>=7.14.0',
 'ipywidgets>=7.5.1',
 'isort>=4.3.21',
 'matplotlib>=3.2.1',
 'mordred>=1.2.0',
 'numpy>=1.18.4',
 'pandas>=1.0.3',
 'plotly>=4.8.0',
 'pubchempy>=1.0.4',
 'quantities>=0.12.4',
 'requests>=2.20.0',
 'scikit-learn>=0.23.1',
 'scipy>=1.4.1',
 'sympy>=1.6',
 'toml>=0.10.2',
 'tqdm>=4.46.0']

setup_kwargs = {
    'name': 'pyrfume',
    'version': '0.16',
    'description': 'A validation library for human olfactory psychophysics research.',
    'long_description': '# Pyrfume\n\n![Pyrfume logo](https://avatars3.githubusercontent.com/u/34174393?s=200&v=4)\n\n#### `pyrfume` is a python library for olfactory psychophysics research. See "notebooks" for examples of use.\n[![Travis](https://travis-ci.org/pyrfume/pyrfume.svg?branch=master)](https://travis-ci.org/pyrfume/pyrfume) \n[![Coverage Status](https://coveralls.io/repos/github/pyrfume/pyrfume/badge.svg?branch=master)](https://coveralls.io/github/pyrfume/pyrfume?branch=master)\n\n### Examples:\n```\n# Load data for Snitz et al, 2013 (PLOS Computational Biology)\nimport pyrfume\nbehavior = pyrfume.load_data(\'snitz_2013/behavior.csv\')\nmolecules = pyrfume.load_data(\'snitz_2013/molecules.csv\')\n\n# Load data for Bushdid et al, 2014 (Science)\nimport pyrfume\nbehavior = pyrfume.load_data(\'bushdid_2014/behavior.csv\')\nmolecules = pyrfume.load_data(\'bushdid_2014/molecules.csv\')\nmixtures = pyrfume.load_data(\'bushdid_2014/behavior.csv\')\n```\n\n### [Website](http://pyrfume.org)\n\n### [Data Curation Status](http://status.pyrfume.org)\n\n### [Docs](https://pyrfume.readthedocs.io/)\n',
    'author': 'Rick Gerkin',
    'author_email': 'rgerkin@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://pyrfume.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
