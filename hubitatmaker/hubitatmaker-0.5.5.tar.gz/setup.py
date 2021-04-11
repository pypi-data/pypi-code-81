# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hubitatmaker', 'hubitatmaker.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'getmac>=0.8.2,<0.9.0']

entry_points = \
{'console_scripts': ['init = scripts:init',
                     'publish = scripts:publish',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'hubitatmaker',
    'version': '0.5.5',
    'description': 'A library for interfacing with Hubitat via its Maker API',
    'long_description': '# hubitatmaker\n\nThis library provides an async Python interface for Hubitat Elevation’s Maker API. It is primarily intended for use with Home Assistant.\n\n## Features\n\nThe main public API in hubitatmaker is the Hub class. This class represents a Maker API instance on a Hubitat hub. When started, a Hub instance will determine the Hubitat hub\'s MAC address and and download a list of available devices and details about each device.\n\nThe Hub instance caches state information about each device. It relies on events posted from the Hubitat hub to update its internal state. Each Hub instance starts a new event listener server to receive events from the hub, and updates the Maker API instance with an accessible URL for this listener server.\n\n## Basic usage\n\n```python\nimport asyncio\nfrom hubitatmaker import Hub\n\nasync def print_devices(host, app_id, token):\n\thub = Hub(host, app_id, token)\n\tawait hub.start()\n\tfor device in hub.devices:\n\t\tprint(f"{device.name} ({device.id})")\n\nif __name__ == \'__main__\':\n\thost = \'http://10.0.1.99\'\n\tapp_id = \'1234\'\n\ttoken = \'<apitoken>\'\n\tasyncio.run(print_devices(host, app_id, token))\n```\n\n## API\n\nSee the [API doc](doc/api.md).\n\n## Developing\n\nTo get setup for development, run\n\n```\n$ poetry run init\n```\n\nTo test the code, which will type check it and run unit tests, run\n\n```\n$ poetry run test\n```\n',
    'author': 'Jason Cheatham',
    'author_email': 'jason@jasoncheatham.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jason0x43/hubitatmaker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
