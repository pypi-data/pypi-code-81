# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycapsule', 'pycapsule.client']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.0,<2.0.0', 'numpy>=1.18.5,<2.0.0']

setup_kwargs = {
    'name': 'pycapsule',
    'version': '0.0.3',
    'description': 'Various tools for Capsule BCI system',
    'long_description': None,
    'author': 'Yaroslav Shmelev',
    'author_email': 'ysh@impulse-machine.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
