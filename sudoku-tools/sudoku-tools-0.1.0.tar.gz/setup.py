# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sudoku', 'sudoku.examples', 'sudoku.solvers', 'sudoku.strategies']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0']

entry_points = \
{'console_scripts': ['sudoku-tools = sudoku.__main__:main']}

setup_kwargs = {
    'name': 'sudoku-tools',
    'version': '0.1.0',
    'description': 'A collection of useful tools for generating, grading, solving, and transforming sudoku puzzles',
    'long_description': '# `sudoku-tools`\n\n[![pypi version](https://img.shields.io/pypi/v/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![downloads](https://pepy.tech/badge/sudoku-tools)](https://pepy.tech/project/sudoku-tools)\n[![build status](https://github.com/dawsonbooth/sudoku-tools/workflows/build/badge.svg)](https://github.com/dawsonbooth/sudoku-tools/actions?workflow=build)\n[![python versions](https://img.shields.io/pypi/pyversions/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![format](https://img.shields.io/pypi/format/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![license](https://img.shields.io/pypi/l/sudoku-tools.svg?style=flat)](https://github.com/dawsonbooth/sudoku-tools/blob/master/LICENSE)\n\n## Description\n\nThis Python package is a collection of useful tools for generating, grading, solving, and transforming sudoku puzzles.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npython -m pip install sudoku-tools\n```\n\n## Usage\n\nThe object can be constructed with a 1-dimensional board:\n\n```python\narr_1d = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]\npuzzle = Puzzle(arr_1d, 0)\n```\n\nFeel free to [check out the docs](https://dawsonbooth.github.io/sudoku-tools/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/sudoku-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
