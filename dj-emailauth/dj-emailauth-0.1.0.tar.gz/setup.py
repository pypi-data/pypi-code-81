# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_emailauth']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0']

setup_kwargs = {
    'name': 'dj-emailauth',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Hloska',
    'author_email': 'martin.hloska@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
