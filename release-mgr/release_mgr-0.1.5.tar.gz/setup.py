# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['release_mgr', 'release_mgr.version_files']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['release-mgr = release_mgr.cli:main']}

setup_kwargs = {
    'name': 'release-mgr',
    'version': '0.1.5',
    'description': 'A simple tool for managing software releases on GitHub.',
    'long_description': None,
    'author': 'Mathew Robinson',
    'author_email': 'mathew@chasinglogic.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
