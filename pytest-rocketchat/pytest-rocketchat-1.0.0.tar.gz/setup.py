# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_rocketchat']

package_data = \
{'': ['*']}

install_requires = \
['rocketchat-API']

entry_points = \
{'pytest11': ['pytest-rocketchat = pytest_rocketchat.plugin']}

setup_kwargs = {
    'name': 'pytest-rocketchat',
    'version': '1.0.0',
    'description': 'Pytest to Rocket.Chat reporting plugin',
    'long_description': '# pytest-rocketchat\nInspired by pytest-slack & pytest-messenger.\n\nPytest to RocketChat reporting plugin\n\n## Requirements\n- Python >= 3.6\n\n## Installation\nYou can install "pytest-rocketchat" via [pip](https://pypi.python.org/pypi/pip/):\n```\n$ pip install pytest-rocketchat\n```\nIf you encounter any problems, please file an [issue](https://github.com/aleksandr-kotlyar/pytest-rocketchat/issues) along with a detailed description.\n',
    'author': 'Aleksandr Kotlyar',
    'author_email': 'ask.kotlyar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/aleksandr-kotlyar/pytest-rocketchat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
