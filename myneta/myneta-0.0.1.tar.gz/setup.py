# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myneta']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'html5lib>=1.1,<2.0',
 'ipython>=7.22.0,<8.0.0',
 'lxml>=4.6.3,<5.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'myneta',
    'version': '0.0.1',
    'description': 'A CLI to interact/extract data from myneta',
    'long_description': None,
    'author': 'kracekumar',
    'author_email': 'me@kracekumar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
