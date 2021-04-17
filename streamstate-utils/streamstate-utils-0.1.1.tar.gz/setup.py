# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['streamstate_utils']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow-dataclass>=8.4.1,<9.0.0']

setup_kwargs = {
    'name': 'streamstate-utils',
    'version': '0.1.1',
    'description': 'Utilities for cassandra and spark streaming specifically for streamstate',
    'long_description': None,
    'author': 'Daniel Stahl',
    'author_email': 'danstahl1138@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/StreamState/streamstate-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
