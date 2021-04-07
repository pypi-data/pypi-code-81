# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpytorch', 'jrpytorch.datasets']

package_data = \
{'': ['*'], 'jrpytorch': ['vignettes/*'], 'jrpytorch.datasets': ['data/*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=1,<2',
 'sklearn>=0.0.0,<0.0.1',
 'torch>=1.0,<2.0',
 'torchvision>=0.5.0,<0.6.0',
 'visdom>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'jrpytorch',
    'version': '0.1.7',
    'description': 'Jumping Rivers: PyTorch with Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
