# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monolish_log_viewer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.2,<6.0',
 'argparse>=1.4.0,<2.0.0',
 'numpy>=1.17,<2.0',
 'pandas>=1.0,<2.0']

entry_points = \
{'console_scripts': ['monolish_log_viewer = monolish_log_viewer.__main__:main']}

setup_kwargs = {
    'name': 'monolish-log-viewer',
    'version': '0.1.1',
    'description': 'Logger script',
    'long_description': None,
    'author': 'RICOS Co. Ltd.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
