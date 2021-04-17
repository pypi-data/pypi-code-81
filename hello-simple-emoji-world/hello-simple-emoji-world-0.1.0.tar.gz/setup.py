# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hello_simple_emoji_world']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'hello-simple-emoji-world',
    'version': '0.1.0',
    'description': 'An attempt to create and publish a cross-platform cli app',
    'long_description': None,
    'author': 'Kishan B',
    'author_email': 'kishancs46@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
