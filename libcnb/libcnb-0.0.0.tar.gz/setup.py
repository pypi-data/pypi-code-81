# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libcnb']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'libcnb',
    'version': '0.0.0',
    'description': ' Cloud Native Buildpack API bindings for Python',
    'long_description': '# Python libcnb\n\n\n[![PyPI version](https://badge.fury.io/py/libcnb.svg)](https://badge.fury.io/py/libcnb)\n![versions](https://img.shields.io/pypi/pyversions/libcnb.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/libcnb.svg)](https://github.com/mgancita/libcnb/blob/main/LICENSE)\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n Cloud Native Buildpack API bindings for Python\n\n\n- Free software: Apache-2.0\n- Documentation: https://samj1912.github.io/python-libcnb.\n\n\n## Features\n\n* TODO\n\n## Credits\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://mgancita.github.io/cookiecutter-pypackage/) project template.\n',
    'author': 'Sambhav Kothari',
    'author_email': 'sambhavs.email@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samj1912/python-libcnb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
