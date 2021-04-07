# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forsyde', 'forsyde.io', 'forsyde.io.python', 'forsyde.io.python.sql']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6,<5.0', 'networkx>=2.5,<3.0', 'pydot>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'forsyde-io-python',
    'version': '0.2.7',
    'description': 'Python supporting libraries for ForSyDe IO',
    'long_description': None,
    'author': 'Rodolfo',
    'author_email': 'jordao@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
