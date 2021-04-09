# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chinormfilter']

package_data = \
{'': ['*']}

install_requires = \
['sudachidict_core>=20201223.post1,<20201224',
 'sudachidict_full>=20201223.post1,<20201224',
 'sudachipy>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['chinormfilter = chinormfilter.cli:cli']}

setup_kwargs = {
    'name': 'chinormfilter',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
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
