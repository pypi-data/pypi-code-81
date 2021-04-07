# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forsyde', 'forsyde.io', 'forsyde.io.python', 'forsyde.io.python.sql']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0', 'pydot>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'forsyde-io-python',
    'version': '0.2.8',
    'description': 'Python supporting libraries for ForSyDe IO',
    'long_description': '# ForSyDe IO Python library\n\nPython Supporting library for ForSyDe IO. \nCheck the [documentation website](https://forsyde.github.io/forsyde-io/) for more info!.\n\n',
    'author': 'Rodolfo',
    'author_email': 'jordao@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://forsyde.github.io/forsyde-io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
