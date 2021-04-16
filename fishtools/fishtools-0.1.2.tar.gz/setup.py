# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fishtools']

package_data = \
{'': ['*']}

install_requires = \
['dtoolbioimage>=0.1.9,<0.2.0',
 'pandas>=1.0.5,<2.0.0',
 'parse>=1.16.0,<2.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['fishtools-process = '
                     'fishtools.process:process_from_config']}

setup_kwargs = {
    'name': 'fishtools',
    'version': '0.1.2',
    'description': 'Tools for analysing FISH data.',
    'long_description': None,
    'author': 'Matthew Hartley',
    'author_email': 'mhartley@cantab.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
