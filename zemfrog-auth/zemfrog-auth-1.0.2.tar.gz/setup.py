# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_auth', 'zemfrog_auth.jwt']

package_data = \
{'': ['*']}

install_requires = \
['zemfrog>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'zemfrog-auth',
    'version': '1.0.2',
    'description': 'Authentication for the zemfrog framework',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
