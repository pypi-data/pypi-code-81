# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['perturbator',
 'perturbator.commands',
 'perturbator.language_parser',
 'perturbator.support_modules']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.0.3,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'textX>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['perturbator = perturbator.perturbator:main']}

setup_kwargs = {
    'name': 'perturbator',
    'version': '0.1.0',
    'description': 'Tool to apply change patterns on Business Process Models',
    'long_description': None,
    'author': 'Zohaib Ahmed Butt',
    'author_email': 'zohaibahmedbutt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
