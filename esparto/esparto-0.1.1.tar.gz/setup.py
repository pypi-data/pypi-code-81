# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esparto']

package_data = \
{'': ['*'], 'esparto': ['templates/*']}

install_requires = \
['Pillow>=7.0.0,<8.0.0', 'jinja2>=2.10.1,<3.0.0', 'markdown>=3.1,<4.0']

extras_require = \
{'extras': ['beautifulsoup4>=4.9.3,<5.0.0']}

setup_kwargs = {
    'name': 'esparto',
    'version': '0.1.1',
    'description': 'Minimal frontend web framework written in Python.',
    'long_description': 'esparto\n=======\n\n[![image](https://img.shields.io/pypi/v/esparto.svg)](https://pypi.python.org/pypi/esparto)\n[![Build Status](https://travis-ci.com/domvwt/esparto.svg?branch=main)](https://travis-ci.com/domvwt/esparto)\n[![codecov](https://codecov.io/gh/domvwt/esparto/branch/main/graph/badge.svg?token=35J8NZCUYC)](https://codecov.io/gh/domvwt/esparto)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=domvwt_esparto&metric=alert_status)](https://sonarcloud.io/dashboard?id=domvwt_esparto)\n\nEsparto is a minimal frontend web framework written in Python. \nIt aims to be the first choice for designing self-contained documents with productivity as the main concern.\n\nFull documentation available at [domvwt.github.io/esparto/](https://domvwt.github.io/esparto/).\n\n### Features \n* Lightweight API\n* No CSS or HTML required\n* Device responsive display\n* Self contained / inline dependencies\n* Jupyter Notebook support\n* MIT License\n',
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://domvwt.github.io/esparto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
