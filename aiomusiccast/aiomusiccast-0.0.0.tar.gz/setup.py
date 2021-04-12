# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiomusiccast']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aiomusiccast',
    'version': '0.0.0',
    'description': 'Companion library for musiccast devices intended for the Home Assistant integration.',
    'long_description': '# Overview\n\nCompanion library for musiccast devices intended for the Home Assistant integration.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/com/vigonotion/template-python-demo.svg?label=unix)](https://travis-ci.com/vigonotion/template-python-demo)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/vigonotion/template-python-demo.svg?label=windows)](https://ci.appveyor.com/project/vigonotion/template-python-demo)\n[![Coverage Status](https://img.shields.io/coveralls/vigonotion/template-python-demo.svg)](https://coveralls.io/r/vigonotion/template-python-demo)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/vigonotion/template-python-demo.svg)](https://scrutinizer-ci.com/g/vigonotion/template-python-demo)\n[![PyPI Version](https://img.shields.io/pypi/v/aiomusiccast.svg)](https://pypi.org/project/aiomusiccast)\n[![PyPI License](https://img.shields.io/pypi/l/aiomusiccast.svg)](https://pypi.org/project/aiomusiccast)\n\n# Setup\n\n## Requirements\n\n* Python 3.8+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install aiomusiccast\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add aiomusiccast\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import aiomusiccast\n>>> aiomusiccast.__version__\n```\n',
    'author': 'Tom Schneider',
    'author_email': 'mail@vigonotion.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/aiomusiccast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
