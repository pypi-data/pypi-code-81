# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_console']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'psutil>=5.8.0,<6.0.0',
 'royalnet>=6.2.0,<6.3.0']

setup_kwargs = {
    'name': 'royalnet-console',
    'version': '2.0.0',
    'description': 'A terminal-based frontend for the royalnet.engineer module.',
    'long_description': '# `royalnet_console`\n\nA terminal-based frontend for the `royalnet.engineer` module.\n\nThe documentation is [hosted on Read The Docs](https://royalnet-console.readthedocs.io/en/latest/).\n\n## See also\n\n- [Royalnet 6](https://github.com/Steffo99/royalnet-6)\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalnet-console',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
