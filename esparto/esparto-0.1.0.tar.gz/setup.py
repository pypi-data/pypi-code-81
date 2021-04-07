# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esparto']

package_data = \
{'': ['*'], 'esparto': ['templates/*']}

install_requires = \
['Pillow>=7.0.0,<8.0.0', 'jinja2>=2.10.1,<3.0.0', 'markdown>=3.1,<4.0']

extras_require = \
{'extras': ['beautifulsoup4>=4.9.3,<5.0.0']}

setup_kwargs = {
    'name': 'esparto',
    'version': '0.1.0',
    'description': 'Simple toolkit for building accessible and shareable HTML documents.',
    'long_description': None,
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
