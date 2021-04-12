# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nte']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['note = nte.main:app', 'nte = nte.main:app']}

setup_kwargs = {
    'name': 'nte',
    'version': '0.0.2',
    'description': 'A CLI scratch pad for notes, commands, lists, etc',
    'long_description': 'nte\n_________________\n\n[![PyPI version](https://badge.fury.io/py/nte.svg)](http://badge.fury.io/py/nte)\n[![Test Status](https://github.com/timothycrosley/nte/workflows/Test/badge.svg?branch=develop)](https://github.com/timothycrosley/nte/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/timothycrosley/nte/workflows/Lint/badge.svg?branch=develop)](https://github.com/timothycrosley/nte/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/timothycrosley/nte/branch/main/graph/badge.svg)](https://codecov.io/gh/timothycrosley/nte)\n[![Join the chat at https://gitter.im/timothycrosley/nte](https://badges.gitter.im/timothycrosley/nte.svg)](https://gitter.im/timothycrosley/nte?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/nte/)\n[![Downloads](https://pepy.tech/badge/nte)](https://pepy.tech/project/nte)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/nte/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/nte/)\n_________________\n\n**nte** A CLI scratch pad for notes, commands, lists, etc\n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
