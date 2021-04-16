# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mockerpy', 'mockerpy.services']

package_data = \
{'': ['*']}

install_requires = \
['docker']

setup_kwargs = {
    'name': 'mockerpy',
    'version': '0.1.0',
    'description': 'Mock client for Docker-py',
    'long_description': None,
    'author': 'Procedural.build',
    'author_email': 'admin@procedural.build',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
