# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roombapy']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['roomba-connect = roombapy.entry_points:connect',
                     'roomba-discovery = roombapy.entry_points:discovery',
                     'roomba-password = roombapy.entry_points:password']}

setup_kwargs = {
    'name': 'roombapy',
    'version': '1.6.3',
    'description': 'Python program and library to control Wi-Fi enabled iRobot Roombas',
    'long_description': '# roombapy\n\n[![CI](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml/badge.svg)](https://github.com/pschmitt/roombapy/actions/workflows/ci.yaml)\n![PyPI](https://img.shields.io/pypi/v/roombapy)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/roombapy)\n![PyPI - License](https://img.shields.io/pypi/l/roombapy)\n\nUnofficial iRobot Roomba python library (SDK).\n\nFork of [NickWaterton/Roomba980-Python](https://github.com/NickWaterton/Roomba980-Python)\n\nThis library was created for the [Home Assistant Roomba integration](https://www.home-assistant.io/integrations/roomba/).\n\n# Installation\n\n```shell\npip install roombapy\n```\n\n# Notes\n\nThis library is only for firmware 2.x.x [Check your robot version!](http://homesupport.irobot.com/app/answers/detail/a_id/529) \n\nOnly local connections are supported.\n\n# How to get your username/blid and password\n\nTo get password from Roomba type in console:\n\n```shell\n$ roomba-password <ip>\n```\n\nIt will find your Roomba in local network, then follow the instructions in console to get password.\nIf IP address not provided password will be request for auto discovered robot. \n\nAlso you can just ask Roomba for info:\n\n```shell\n$ roomba-discovery <optional ip address>\n```\n\nTo test connection with iRobot:\n\n```shell\n$ roomba-connect <ip> <password>\n```\n',
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pschmitt/roombapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
