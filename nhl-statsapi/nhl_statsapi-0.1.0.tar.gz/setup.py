# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nhl_statsapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nhl-statsapi',
    'version': '0.1.0',
    'description': 'NHL Stats API',
    'long_description': '# NHL Stats API\n\n### Shields\n\n## Introduction\n\n## Installation\n\n## Usage\n\n## Code of Conduct\n\n## Changelog\n',
    'author': 'munsterberg',
    'author_email': 'jetrussell93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Munsterberg/nhl_statsapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
