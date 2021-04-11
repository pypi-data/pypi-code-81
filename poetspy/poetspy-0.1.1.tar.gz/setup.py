# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetspy']

package_data = \
{'': ['*'], 'poetspy': ['__snapshots__/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'loguru>=0.5.3,<0.6.0',
 'marko>=1.0.1,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['pt = poetspy.poets:main', 'ptg = poetspy.generate:main']}

setup_kwargs = {
    'name': 'poetspy',
    'version': '0.1.1',
    'description': 'A small cli util to show project directories',
    'long_description': "# Poets\n\nA small script that goes over the directories of the current directories, and print them\n`ls`-like, but also showing descriptions scraped to the best of the script's abilities\n\n![demonstration](./assets/demonstration.gif)\n\n## Getting Started\n\nInstallation with pip\n\n```bash\n$ pip install poetspy\n```\n\nInstallation with pipx\n\n```bash\n$ pipx install poetspy\n```\n\n## Usage\n\n`cd` into your directory containing all your projects, then `pt`\n",
    'author': 'JokeNeverSoke',
    'author_email': 'zengjoseph@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jokeneversoke/poets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
