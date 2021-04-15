# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['act_police_archiver']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'lxml>=4.6.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'act-police-archiver',
    'version': '1.0.2',
    'description': 'Archive ACT Policing Media Releases',
    'long_description': None,
    'author': 'king-millez',
    'author_email': 'Millez.Dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
