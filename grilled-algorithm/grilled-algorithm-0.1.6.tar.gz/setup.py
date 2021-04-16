# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grilled', 'grilled.algorithm']

package_data = \
{'': ['*']}

install_requires = \
['grilled-common>=0.1.1,<0.2.0',
 'pandas>=1.2.3,<2.0.0',
 'python-dotenv>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'grilled-algorithm',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'hans',
    'author_email': 'dxzenghan@163.com',
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
