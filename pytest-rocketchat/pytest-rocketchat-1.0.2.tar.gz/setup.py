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
    'version': '1.0.2',
    'description': 'Pytest to Rocket.Chat reporting plugin',
    'long_description': '# pytest-rocketchat\nPytest to [RocketChat](https://github.com/RocketChat) reporting plugin.\n\n[![pypi](https://img.shields.io/pypi/v/pytest-rocketchat.svg)](https://pypi.org/project/pytest-rocketchat/)\n\n___Inspired by [pytest-slack](https://pypi.org/project/pytest-slack/) & [pytest-messenger](https://pypi.org/project/pytest-messenger/).___\n\n## Usage\n```\n$ pytest --rocketchat_server_url=https://your.chat --rocketchat_username=username --rocketchat_password=password\n```\nOptions:\n- --rocketchat_server_url* (Required)\n- --rocketchat_username* (Required)\n- --rocketchat_password* (Required)\n- --rocketchat_report_link\n- --rocketchat_message_prefix\n- --rocketchat_timeout\n- --rocketchat_success_emoji\n- --rocketchat_failed_emoji\n- --ssl_verify\n\n## Requirements\n- Python >= 3.6\n\n## Installation\nYou can install "pytest-rocketchat" via [pip](https://pypi.python.org/pypi/pip/):\n```\n$ pip install pytest-rocketchat\n```\nIf you encounter any problems, please file an [issue](https://github.com/aleksandr-kotlyar/pytest-rocketchat/issues) along with a detailed description.\n',
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
