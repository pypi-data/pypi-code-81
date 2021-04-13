# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiosignalrcore',
 'aiosignalrcore.hub',
 'aiosignalrcore.messages',
 'aiosignalrcore.messages.handshake',
 'aiosignalrcore.protocol',
 'aiosignalrcore.protocol.handshake',
 'aiosignalrcore.transport',
 'aiosignalrcore.transport.websockets']

package_data = \
{'': ['*']}

install_requires = \
['msgpack==1.0.2', 'requests>=2.22.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'aiosignalrcore',
    'version': '0.9.2',
    'description': 'Async fork of Python SignalR Core client(json and messagepack), with invocation auth and two way streaming. Compatible with azure / serverless functions. Also with automatic reconnect and manually reconnect.',
    'long_description': '# SignalR core client (async fork)\n![Pypi](https://img.shields.io/pypi/v/aiosignalrcore.svg)\n\nThis is asyncio version of the original SignalR Core [library](https://github.com/mandrewcito/signalrcore).  \nThe main difference is that `websocket` library is replaced with asyncio-compatabile `websockets`.  \nAll future changes in the original repo will be merged to this fork inheriting the major and minor version number.',
    'author': 'mandrewcito',
    'author_email': 'anbaalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dipdup-net/aiosignalrcore',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
