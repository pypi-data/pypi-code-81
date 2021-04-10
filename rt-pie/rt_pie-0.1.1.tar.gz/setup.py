# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rt_pie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rt-pie',
    'version': '0.1.1',
    'description': 'Real Rime PItch Estimator',
    'long_description': '# RT PIE<br>Real Time PItch Estimator\n\n[**pypi link**](https://pypi.org/project/rt-pie)\n\n## Installation\n\n    pip install rt_pie\n\n## Usage\n\n    from rt_pie import hello_world \n\n    hello_world.greet()\n\n## Development\n\nDownload sources\n\n    git clone ...\n\nInstall dependencies\n\n    poetry install\n\n### Build / Publish\n\n    poetry build\n    poetry publish\n\n#### Authors\nKaspar Wolfisberg<br>\nLuca Di Lanzo\n\n',
    'author': 'Kaspar Wolfisberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wolfisberg/rt-pie',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
