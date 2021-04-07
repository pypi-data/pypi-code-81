# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['knightstour', 'knightstour.modules.knightstour']

package_data = \
{'': ['*'], 'knightstour': ['modules/*']}

setup_kwargs = {
    'name': 'knightstour',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lucas McGregor',
    'author_email': 'lucasmcgregor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
