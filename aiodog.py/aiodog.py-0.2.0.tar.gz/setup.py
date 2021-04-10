# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodog']

package_data = \
{'': ['*']}

install_requires = \
['dog.py>=0.2.0,<0.3.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'aiodog.py',
    'version': '0.2.0',
    'description': 'An async wrapper for https://pypi.org/projects/dog.py which covers all of https://thedogapi.com/',
    'long_description': None,
    'author': 'ToxicKidz',
    'author_email': '78174417+ToxicKidz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
