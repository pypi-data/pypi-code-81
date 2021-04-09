# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['normie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'normie',
    'version': '0.1.0',
    'description': 'Accurate and efficient normal distribution statistics.',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
