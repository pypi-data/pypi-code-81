# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['webbot']

package_data = \
{'': ['*'],
 'webbot': ['drivers/chrome_linux',
            'drivers/chrome_linux',
            'drivers/chrome_linux',
            'drivers/chrome_mac',
            'drivers/chrome_mac',
            'drivers/chrome_mac',
            'drivers/chrome_windows.exe',
            'drivers/chrome_windows.exe',
            'drivers/chrome_windows.exe']}

install_requires = \
['selenium>=3.141.0,<4.0.0']

entry_points = \
{'console_scripts': ['oronium = webbot.webbot:main']}

setup_kwargs = {
    'name': 'oronium',
    'version': '0.1.3',
    'description': 'Webbot selenium driver for testing openremote',
    'long_description': None,
    'author': 'Michal Rutka',
    'author_email': 'michal@openremote.io',
    'maintainer': 'OpenRemote',
    'maintainer_email': 'developers@openremote.io',
    'url': 'https://github.com/aktur/webbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
