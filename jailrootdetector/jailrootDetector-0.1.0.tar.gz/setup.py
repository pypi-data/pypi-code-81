# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jailrootdetector']

package_data = \
{'': ['*']}

install_requires = \
['r2pipe>=1.5.3,<2.0.0', 'sh>=1.14.1,<2.0.0']

entry_points = \
{'console_scripts': ['jrd = jailrootdetector.main:main']}

setup_kwargs = {
    'name': 'jailrootdetector',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JxTx',
    'author_email': 'joethorpe6@protonmail.com',
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
