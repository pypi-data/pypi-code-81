# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rdfox_runner']

package_data = \
{'': ['*']}

install_requires = \
['rdflib>=5.0.0,<6.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'rdfox-runner',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Rick Lupton',
    'author_email': 'mail@ricklupton.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
