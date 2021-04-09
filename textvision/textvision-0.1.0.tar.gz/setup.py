# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textvision']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'google-cloud-vision>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['textvision = textvision.detectors:detect']}

setup_kwargs = {
    'name': 'textvision',
    'version': '0.1.0',
    'description': 'textvision uses the Google Vision API to perform OCR and return text.',
    'long_description': None,
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
