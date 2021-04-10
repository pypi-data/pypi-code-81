# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsort']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['reqsort = rsort.main:app', 'rsort = rsort.main:app']}

setup_kwargs = {
    'name': 'rsort',
    'version': '0.1.1',
    'description': 'Sort requirements with ease! 🎉',
    'long_description': '<h1 align="center">\n    <strong>rsort</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/rsort" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/rsort" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/rsort/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/rsort">\n    <br />\n    <a href="https://pypi.org/project/rsort" target="_blank">\n        <img src="https://img.shields.io/pypi/v/rsort" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/rsort">\n    <img src="https://img.shields.io/github/license/Kludex/rsort">\n</p>\n\n\n## Installation\n\n``` bash\npip install rsort\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/rsort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
