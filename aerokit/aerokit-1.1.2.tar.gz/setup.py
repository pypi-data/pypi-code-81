# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerokit',
 'aerokit.aero',
 'aerokit.aero.plot',
 'aerokit.common',
 'aerokit.engine',
 'aerokit.instance']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.4,<2.0.0', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'aerokit',
    'version': '1.1.2',
    'description': 'Python tools for basic fluid mechanics computations',
    'long_description': None,
    'author': 'j.gressier',
    'author_email': 'jeremie.gressier@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jgressier/aerokit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
