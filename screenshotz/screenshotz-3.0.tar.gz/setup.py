# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screenshotz']

package_data = \
{'': ['*']}

install_requires = \
['Pillow', 'pyyaml', 'selenium']

entry_points = \
{'console_scripts': ['screenshotz = screenshotz:command.do_command']}

setup_kwargs = {
    'name': 'screenshotz',
    'version': '3.0',
    'description': 'Basic screenshot scripting',
    'long_description': '# `screenshotz`: Easy screenshot scripting\n',
    'author': 'Robert Lechte',
    'author_email': 'robert.lechte@dpc.vic.gov.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
