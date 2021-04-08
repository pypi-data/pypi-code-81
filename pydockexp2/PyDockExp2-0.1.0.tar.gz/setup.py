# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydockexp2',
 'pydockexp2.config',
 'pydockexp2.funcs',
 'pydockexp2.iterator',
 'pydockexp2.util']

package_data = \
{'': ['*'], 'pydockexp2.config': ['sample/*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'coloredlogs>=15.0,<16.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'rich>=10.1.0,<11.0.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'pydockexp2',
    'version': '0.1.0',
    'description': 'A simple random matrix generato',
    'long_description': None,
    'author': 'lmriccardo',
    'author_email': 'absintio098@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lmriccardo/PyDocker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
