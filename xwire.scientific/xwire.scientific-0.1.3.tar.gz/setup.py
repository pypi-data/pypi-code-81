# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xwire',
 'xwire.scientific',
 'xwire.scientific._private',
 'xwire.scientific._private.data',
 'xwire.scientific._private.math',
 'xwire.scientific._private.model',
 'xwire.scientific.public']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.1,<2.0.0', 'pandas>=1.2.3,<2.0.0', 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'xwire.scientific',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'tylerlaberge',
    'author_email': 'tylerlaberge@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
