# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolt_integrations',
 'dolt_integrations.metaflow',
 'dolt_integrations.metaflow.examples.hospital_bounty',
 'dolt_integrations.utils']

package_data = \
{'': ['*']}

install_requires = \
['doltcli>=0.1.4,<0.2.0', 'pandas>=0.25.2']

extras_require = \
{'metaflow': ['metaflow>=2.2.6,<3.0.0']}

setup_kwargs = {
    'name': 'dolt-integrations',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Max Hoffman',
    'author_email': 'max@dolthub.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
