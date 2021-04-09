# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scpi',
 'scpi.devices',
 'scpi.errors',
 'scpi.transports',
 'scpi.transports.gpib']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'scpi',
    'version': '2.3.1',
    'description': 'Basic idea here is to make transport-independent command sender/parser and a device baseclass that implements the common SCPI commands',
    'long_description': "====\nscpi\n====\n\nNew asyncio_ version. Only for Python 3.6 and above\n\nSince all the other wrappers either require VISA binary or are not generic (and do not implement the device I need)\n\nBasic idea here is to make transport-independent command sender/parser and a device baseclass that implements the common SCPI commands\n\nA device specific implementation can then add the device-specific commands.\n\nPro tip for thos wishing to work on the code https://python-poetry.org/\n\n.. _asyncio: https://docs.python.org/3/library/asyncio.html\n\n\n## Usage\n\nInstall the package to your virtualenv with poetry or from pip\n\n  - Instatiate a transport (for GPIB you will need `GPIBDeviceTransport` to be able to use the device helper class)\n  - Instatiate `SCPIProtocol` with the transport (optional, see below)\n  - Instantiate `SCPIDevice` with the protocol (or as a shorthand: with the transport directly)\n  - Use the asyncio eventloop to run the device methods (all of which are coroutines)\n\nOr if you're just playing around in the REPL use `AIOWrapper` to hide the eventloop handling\nfor traditional non-concurrent approach.\n\nSee the examples directory for more.\n\nTODO\n----\n\nCheck Carrier-Detect for RS232 transport\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nin the RS232 transport check getCD to make sure the device is present before doing anything.\nCTS can also be checked even if hw flow control is not in use.\n\nBasically wait for it for X seconds and abort if not found\n",
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rambo/python-scpi/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
