# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rgs', 'rgs.mndrpy', 'rgs.pmaps', 'rgs.ribbons', 'rgs.slimtree']

package_data = \
{'': ['*']}

install_requires = \
['numdifftools']

setup_kwargs = {
    'name': 'rgs',
    'version': '0.1.8',
    'description': 'A small package to display and manipulate random geometry structures like pairings, meanders, triangulations and tilings.',
    'long_description': '# RandomGeometricStructures\nA collection of various function to draw and analyze random geometric structures (like pairings, tilings etc.)\n\nAn illustration can be found at: \n\nFor pmaps package:\n[Triangulations](https://colab.research.google.com/drive/1URQte3-X6Lau74B0JSjU7gkStO_-kx0O?usp=sharing )\n',
    'author': 'Vladislav Kargin',
    'author_email': 'slavakargin@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slavakargin/RandomGeeometricStructures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
