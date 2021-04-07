# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cheminfopy', 'cheminfopy.managers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cheminfopy',
    'version': '0.2.0',
    'description': 'cheminfopy is a SDK that provides a high-level interface to the rest-on-couch API that powers the cheminfo ELN',
    'long_description': '# cheminfopy\n\n[![Documentation Status](https://readthedocs.org/projects/cheminfopy/badge/?version=latest)](https://cheminfopy.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cheminfopy)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n![GitHub last commit](https://img.shields.io/github/last-commit/cheminfo-py/cheminfopy)\n\n<!-- ![Python package](https://github.com/cheminfo-py/pytojcamp/workflows/Python%20package/badge.svg)\n![pre-commit](https://github.com/cheminfo-py/pytojcamp/workflows/pre-commit/badge.svg)\n[![codecov](https://codecov.io/gh/cheminfo-py/pytojcamp/branch/master/graph/badge.svg)](https://codecov.io/gh/cheminfo-py/pytojcamp) -->\n\n> A Python interface to interact with the [cheminfo electronic lab notebook](https://cheminfo.github.io/eln.epfl.ch/)\n\nThe data schema of the ELN is described on a [separate webpage](https://cheminfo.github.io/data_schema/).\n\n**This package is still in exploratory development and the API is not stable**\n',
    'author': 'Kevin M. Jablonka',
    'author_email': 'kevin.jablonka@epfl.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cheminfo-py/cheminfopy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
