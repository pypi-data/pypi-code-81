# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitm_chrome']

package_data = \
{'': ['*']}

install_requires = \
['mitmproxy>=6,<7']

entry_points = \
{'console_scripts': ['mitm_chrome = mitm_chrome:cli']}

setup_kwargs = {
    'name': 'mitm-chrome',
    'version': '0.1.2',
    'description': 'Integrate chrome with mitmproxy.',
    'long_description': "# mitm chrome\n\nIntegrate chrome with [mitmproxy](https://mitmproxy.org/).\n\n## installation\n\n```shell\npip install mitm_chrome\n```\n\n## Usage\n\nOn MacOS\n\n```shell\nmitm_chrome --chrome-path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' mitmproxy\n```\n\nElse\n\n```shell\nmitm_chrome mitmproxy\n```\n",
    'author': '林玮 (Jade Lin)',
    'author_email': 'linw1995@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linw1995/mitm_chrome',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
