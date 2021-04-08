# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thingtalk',
 'thingtalk.domains',
 'thingtalk.models',
 'thingtalk.routers',
 'thingtalk.toolkits']

package_data = \
{'': ['*']}

install_requires = \
['async-cron>=1.6.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'dynaconf>=3.1.2,<4.0.0',
 'email_validator>=1.1.1,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'gmqtt>=0.6.9,<0.7.0',
 'httpx>=0.17.0,<0.18.0',
 'ifaddr>=0.1.7,<0.2.0',
 'jsonschema>=3.2.0,<4.0.0',
 'loguru>=0.5.2,<0.6.0',
 'pyee>=8.1.0,<9.0.0',
 'rich>=10.0.0,<11.0.0',
 'ujson>=4.0.0,<5.0.0',
 'uvicorn[standard]>=0.13.0,<0.14.0',
 'zeroconf>=0.29.0,<0.30.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['cached-property>=1.5,<2.0'],
 'docs': ['mkdocs-material>=7.0.0,<8.0.0']}

entry_points = \
{'console_scripts': ['thingtalk = thingtalk.cli:thingtalk']}

setup_kwargs = {
    'name': 'thingtalk',
    'version': '0.8.0',
    'description': 'Web of Things framework, high performance, easy to learn, fast to code, ready for production',
    'long_description': '<h1 align="center">Project thingTalk</h1>\n\n<h2 align="center">Thing as a Service</h2>\n\n[![pypi-v](https://img.shields.io/pypi/v/thingtalk.svg)](https://pypi.python.org/pypi/thingtalk)\n[![python](https://img.shields.io/pypi/pyversions/thingtalk.svg)](https://github.com/hidaris/thingtalk)\n\n## What is `thingTalk`?\n`thingTalk` is a web of things implementation, currently supporting a dialect protocol called webthings.\n\n## Project Vision:\nTo provide a communication layer for spatial computing, and make iot interoperable with xr.\n\n### The key features are:\n* Layered design -- Provide services such as rule engines on top of the core protocol layer.\n* Scalability -- Can be based on MQTT to achieve distributed deployment.\n* Standards-based -- Compatibility with community standards[WoT].\n* Fast: Very high performance, on par with NodeJS and Go (thanks to FastAPI).\n* Robust: Get production-ready code. With automatic interactive documentation.\n* Fast to code: Increase the speed to develop features by about 200% to 300%. *\n\n## Installation\nthingtalk can be installed via pip, as such:\n\n`$ pip install thingtalk`\n',
    'author': 'hidaris',
    'author_email': 'zuocool@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hidaris/thingtalk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
