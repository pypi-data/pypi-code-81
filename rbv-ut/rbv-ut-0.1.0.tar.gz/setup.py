# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rbv_ut', 'rbv_ut.mk']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'cattrs>=1.4.0,<2.0.0',
 'reader-rbv>=0.6.0,<0.7.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'rbv-ut',
    'version': '0.1.0',
    'description': '',
    'long_description': '# rbv-ut\n\nSDK / Client Python Ruang Baca Virtual UT\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
