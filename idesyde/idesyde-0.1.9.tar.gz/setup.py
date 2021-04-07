# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idesyde', 'idesyde.identification', 'idesyde.minizinc']

package_data = \
{'': ['*']}

install_requires = \
['forsyde-io-python>=0.2.7,<0.3.0',
 'minizinc>=0.4,<0.5',
 'numpy>=1.20,<2.0',
 'sympy>=1.7,<2.0']

entry_points = \
{'console_scripts': ['idesyde = idesyde.cli:cli_entry']}

setup_kwargs = {
    'name': 'idesyde',
    'version': '0.1.9',
    'description': 'Generic Design Space Exploration for models based system design',
    'long_description': '# IDeSyDe\n\nThis is the generic Design Space Exploration (DSE) tool associated with the ForSyDe Ecosystem and the spiritual sucessor of [DeSyDe](https://github.com/forsyde/DeSyDe). Check the [documentation website for more information](https://forsyde.github.io/IDeSyDe/)!\n',
    'author': 'jordao',
    'author_email': 'jordao@kth.se',
    'maintainer': 'jordao',
    'maintainer_email': 'jordao@kth.se',
    'url': 'https://forsyde.github.io/IDeSyDe/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
