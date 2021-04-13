# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loopia_of_fury']

package_data = \
{'': ['*']}

install_requires = \
['su-logging[structured]>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['loopia_of_fury = loopia_of_fury:main']}

setup_kwargs = {
    'name': 'loopia-of-fury',
    'version': '1.2.0',
    'description': 'Loopia of Fury - A "DynDNS" client for Loopia when you have MFA/BankID enabled ',
    'long_description': None,
    'author': 'Simon Lundström',
    'author_email': 'github-commits@soy.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simmel/loopia_of_fury',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
