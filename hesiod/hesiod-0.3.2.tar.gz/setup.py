# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hesiod',
 'hesiod.cfg',
 'hesiod.ui',
 'hesiod.ui.tui',
 'hesiod.ui.tui.widgets',
 'hesiod.ui.tui.widgets.custom']

package_data = \
{'': ['*']}

install_requires = \
['asciimatics>=1.12.0,<2.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'typeguard>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'hesiod',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Luca De Luigi',
    'author_email': 'lucadeluigi91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
