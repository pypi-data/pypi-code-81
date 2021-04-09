# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.broadcast',
 'graia.broadcast.builtin',
 'graia.broadcast.entities',
 'graia.broadcast.entities.signatures',
 'graia.broadcast.interfaces',
 'graia.broadcast.interrupt']

package_data = \
{'': ['*']}

install_requires = \
['iterwrapper>=0.1.2,<0.2.0', 'pydantic<=1.7.1']

setup_kwargs = {
    'name': 'graia-broadcast',
    'version': '0.8.11',
    'description': 'a highly customizable, elegantly designed event system based on asyncio',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
