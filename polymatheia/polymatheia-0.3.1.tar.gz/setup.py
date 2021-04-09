# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polymatheia', 'polymatheia.data']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0',
 'lxml>=4.5.2,<5.0.0',
 'munch>=2.5.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'sickle>=0.7.0,<0.8.0',
 'srupy>=0.0.45,<0.0.46']

setup_kwargs = {
    'name': 'polymatheia',
    'version': '0.3.1',
    'description': 'A python library to support digital archive metadata use',
    'long_description': '# Polymatheia\n\n![Validation Status](https://github.com/scmmmh/polymatheia/workflows/Validation/badge.svg) ![Build Status](https://github.com/scmmmh/polymatheia/workflows/Tests/badge.svg) [![Documentation Status](https://readthedocs.org/projects/polymatheia/badge/?version=latest)](https://polymatheia.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/polymatheia.svg)](https://badge.fury.io/py/polymatheia)\n\nPolymatheia is a python library to support working with digital archive metadata. Its aim is not necessarily to cover\nall ways of working with digital archive metadata, but to make it (comparatively) easy to undertake most types of\ntasks and analysis.\n\n*Homepage*: https://polymatheia.readthedocs.io\n\n*Repository*: https://github.com/scmmmh/polymatheia\n\n*Package*: https://pypi.org/project/polymatheia\n\n*License*: MIT\n',
    'author': 'Mark Hall',
    'author_email': 'mark.hall@work.room3b.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://polymatheia.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
