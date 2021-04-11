# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['columnarframe']

package_data = \
{'': ['*']}

install_requires = \
['pyarrow>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'columnarframe',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tamuto',
    'author_email': 'tamuto@infodb.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
