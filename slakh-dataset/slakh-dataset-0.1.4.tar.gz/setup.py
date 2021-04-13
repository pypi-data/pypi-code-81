# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slakh_dataset']

package_data = \
{'': ['*'], 'slakh_dataset': ['splits/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'pretty_midi>=0.2.9,<0.3.0',
 'torch>=1.8.1,<2.0.0',
 'torchaudio>=0.8.1,<0.9.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'slakh-dataset',
    'version': '0.1.4',
    'description': 'Unofficial PyTorch dataset for Slakh',
    'long_description': None,
    'author': 'Henrik Grønbech',
    'author_email': 'henrikgronbech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
