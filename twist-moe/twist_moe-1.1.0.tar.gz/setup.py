# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twist_moe']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome', 'requests']

entry_points = \
{'console_scripts': ['twist = twist_moe.tui:main']}

setup_kwargs = {
    'name': 'twist-moe',
    'version': '1.1.0',
    'description': 'twist.moe client',
    'long_description': None,
    'author': 'witherornot',
    'author_email': 'damemem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
