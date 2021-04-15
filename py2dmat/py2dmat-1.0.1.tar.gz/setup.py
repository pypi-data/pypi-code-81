# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py2dmat', 'py2dmat.algorithm', 'py2dmat.solver']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'toml>=0.10.0']

extras_require = \
{'all': ['scipy>=1,<2', 'mpi4py>=3,<4', 'physbo>=0.3.0'],
 'bayes': ['physbo>=0.3.0'],
 'exchange': ['mpi4py>=3,<4'],
 'min_search': ['scipy>=1,<2']}

entry_points = \
{'console_scripts': ['py2dmat = py2dmat:main']}

setup_kwargs = {
    'name': 'py2dmat',
    'version': '1.0.1',
    'description': 'Data-analysis software of quantum beam diffraction experiments for 2D material structure',
    'long_description': '# 2DMAT -- Data-analysis software of quantum beam diffraction experiments for 2D material structure\n\n2DMAT is a framework for applying a search algorithm to a direct problem solver to find the optimal solution.\nAs the standard direct problem solver, the experimental data analysis software for two-dimensional material structure analysis is prepared.\nThe direct problem solver gives the deviation between the experimental data and the calculated data obtained under the given parameters such as atomic positions as a loss function used in the inverse problem.\nThe optimal parameters are estimated by minimizing the loss function using a search algorithm. For further use, the original direct problem solver or the search algorithm can be defined by users.\nIn the current version, for solving a direct problem, 2DMAT offers the wrapper of the solver for the total-reflection high-energy positron diffraction (TRHEPD) experiment.\nAs algorithms, it offers the Nelder-Mead method, the grid search method, the Bayesian optimization method, and the replica exchange Monte Carlo method. In the future, we plan to add other direct problem solvers and search algorithms in 2DMAT.\n\n| Branch | Build status | Documentation |\n| :-: | :-: | :-: |\n| master | [![master](https://github.com/issp-center-dev/2DMAT/workflows/Test/badge.svg?branch=master)](https://github.com/issp-center-dev/2DMAT/actions?query=branch%3Amaster) | [![doc_en](https://img.shields.io/badge/doc-English-blue.svg)](https://issp-center-dev.github.io/2DMAT/manual/master/en/index.html)  [![doc_ja](https://img.shields.io/badge/doc-Japanese-blue.svg)](https://issp-center-dev.github.io/2DMAT/manual/master/ja/index.html) |\n| v1.0.1 | -- | [![doc_en](https://img.shields.io/badge/doc-English-blue.svg)](https://issp-center-dev.github.io/2DMAT/manual/v1.0.1/en/index.html)  [![doc_ja](https://img.shields.io/badge/doc-Japanese-blue.svg)](https://issp-center-dev.github.io/2DMAT/manual/v1.0.1/ja/index.html) |\n\n## py2dmat\n\n`py2dmat` is a python framework library for solving inverse problems.\nIt also offers a driver script to solve the problem with predefined algorithms\nand solvers (`py2dmat` also means this script).\n\n### Prerequists\n\n- Required\n  - python >= 3.6\n  - numpy >= 1.17\n  - toml\n- Optional\n  - scipy\n    - for `minsearch` algorithm\n  - mpi4py\n    - for `exchange` algorithm\n  - physbo >= 0.3\n    - for `bayes` algorithm\n\n### Install\n\n- From PyPI (Recommended)\n  - `python3 -m pip install py2dmat`\n    - If you install them locally, use `--user` option like `python3 -m pip install --user`\n    - [`pipx`](https://pipxproject.github.io/pipx/) may help you from the dependency hell :p\n- From Source (For developers)\n  1. update `pip >= 19` by `python3 -m pip install -U pip`\n  2. `python3 -m pip install 2DMAT_ROOT_DIRECTORY` to install `py2dmat` package and `py2dmat` command\n\n### Simple Usage\n\n- `py2dmat input.toml` (use the installed script)\n- `python3 src/py2dmat_main.py input.toml` (use the raw script)\n- For details of the input file, see the document.\n\n## License\n\nThis package is distributed under GNU General Public License version 3 (GPL v3) or later.\n\n## Copyright\n\n© *2020- The University of Tokyo. All rights reserved.*\nThis software was developed with the support of \\"*Project for advancement of software usability in materials science*\\" of The Institute for Solid State Physics, The University of Tokyo. \n',
    'author': '2DMAT developers',
    'author_email': '2dmat-dev@issp.u-tokyo.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/issp-center-dev/2DMAT',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
