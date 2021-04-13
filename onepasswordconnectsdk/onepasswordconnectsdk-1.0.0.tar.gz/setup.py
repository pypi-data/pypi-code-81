# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onepasswordconnectsdk', 'onepasswordconnectsdk.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'requests>=2.24.0,<3.0.0', 'six>=1.10,<2.0']

setup_kwargs = {
    'name': 'onepasswordconnectsdk',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': '1Password',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
