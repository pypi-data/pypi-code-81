# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olxbrasil', 'olxbrasil.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'httpx>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'olxbrasil',
    'version': '0.2.4',
    'description': 'Biblioteca para scrapping da Olx Brasil (olx.com.br)',
    'long_description': '# OLX Brasil Scrapping\n\n[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square)](/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/olxbrasil.svg)](https://pypi.python.org/pypi/olxbrasil)\n[![PyPI](https://img.shields.io/pypi/pyversions/olxbrasil.svg)]()\n![PyPI - Downloads](https://img.shields.io/pypi/dm/olxbrasil.svg?label=pip%20installs&logo=python)\n[![codecov](https://codecov.io/gh/mdslino/olxbrasil/branch/main/graph/badge.svg)](https://codecov.io/gh/mdslino/olxbrasil)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/54968a88b27647f1b47154f942905a5d)](https://www.codacy.com/gh/Mdslino/olxbrasil/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Mdslino/olxbrasil&amp;utm_campaign=Badge_Grade)\n![GitHub issues](https://img.shields.io/github/issues/mdslino/olxbrasil.svg)\n![GitHub stars](https://img.shields.io/github/stars/mdslino/olxbrasil.svg)\n![GitHub last commit](https://img.shields.io/github/last-commit/mdslino/olxbrasil.svg)\n[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)\n',
    'author': 'Marcelo Lino',
    'author_email': 'mdslino@gmail.com',
    'maintainer': 'Marcelo Lino',
    'maintainer_email': 'mdslino@gmail.com',
    'url': 'https://github.com/Mdslino/olxbrasil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
