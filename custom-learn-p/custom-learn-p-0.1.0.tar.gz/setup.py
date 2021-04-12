# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['custom_learn_p']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'custom-learn-p',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
