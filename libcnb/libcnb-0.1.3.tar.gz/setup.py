# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libcnb']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0',
 'packaging>=20.9,<21.0',
 'pydantic>=1.8.1,<2.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'libcnb',
    'version': '0.1.3',
    'description': ' Cloud Native Buildpack API bindings for Python',
    'long_description': '# libcnb\n\n\n[![PyPI version](https://badge.fury.io/py/libcnb.svg)](https://badge.fury.io/py/libcnb)\n![versions](https://img.shields.io/pypi/pyversions/libcnb.svg)\n[![GitHub license](https://img.shields.io/github/license/samj1912/libcnb.svg)](https://github.com/samj1912/libcnb/blob/main/LICENSE)\n[![Code Quality Checks](https://github.com/samj1912/python-libcnb/actions/workflows/code_quality_checks.yml/badge.svg)](https://github.com/samj1912/python-libcnb/actions/workflows/code_quality_checks.yml)\n[![Docs publish](https://github.com/samj1912/python-libcnb/actions/workflows/docs_publish.yml/badge.svg)](https://github.com/samj1912/python-libcnb/actions/workflows/docs_publish.yml)\n[![codecov](https://codecov.io/gh/samj1912/python-libcnb/branch/main/graph/badge.svg?token=Vb5svxOpMj)](https://codecov.io/gh/samj1912/python-libcnb)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Downloads](https://static.pepy.tech/personalized-badge/libcnb?period=total&units=international_system&left_color=black&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/libcnb)\n\n Cloud Native Buildpack API bindings for Python\n\n\n- Free software: Apache-2.0\n- Documentation: https://samj1912.github.io/python-libcnb.\n\n## Usage\n\nCheck out the documentation - https://samj1912.github.io/python-libcnb\n\n## Credits\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://mgancita.github.io/cookiecutter-pypackage/) project template.\n',
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
