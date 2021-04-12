# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikitrad']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'langdetect>=1.0.8,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['wikitrad = wikitrad.wikitrad:run']}

setup_kwargs = {
    'name': 'wikitrad',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ewen Le Bihan',
    'author_email': 'hey@ewen.works',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
