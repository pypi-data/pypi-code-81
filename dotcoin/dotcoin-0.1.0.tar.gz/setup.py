# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotcoin',
 'dotcoin.console',
 'dotcoin.context',
 'dotcoin.core',
 'dotcoin.queries',
 'dotcoin.sources',
 'dotcoin.sources.ccxt',
 'dotcoin.tables']

package_data = \
{'': ['*']}

install_requires = \
['beautifultable>=1.0.1,<2.0.0', 'ccxt>=1.47.3,<2.0.0', 'six>=1.15.0,<2.0.0']

entry_points = \
{'console_scripts': ['dotcoin = dotcoin.__main__:main']}

setup_kwargs = {
    'name': 'dotcoin',
    'version': '0.1.0',
    'description': '',
    'long_description': '# DotCoin\n\n## Introduction\n\nDotCoin is an abstract interface build around ccxt to access information on cryptocurrency markets from a variety of\nexchanges/platforms, while being accessible to non-coders or coders who don\'t want to write a program just to check some\nbasic info.\n\nAs of this moment, DotCoin provides a simple cli that can look into the basic stats of some markets and checking their\ncurrent order-book. Please bear in mind that DotCoin is currently just a personal project that just started its\ndevelopment status and needs a lot of time and work to grow.\n\n## Installation\n\nA package with the name "dotcoin" is available in pypi.\n\n````commandline\npip install --user dotcoin \n````\n\nThis package has been tested mainly with **Python 3.7.9** on **Windows 10**, but it should work on all platforms since\nit only makes use of cross-platform libraries. You may need to prefix this command with *"pip3"*, *"python3 -m pip"* or\n*"python -m pip"* instead when running on other platforms or different Python setups.\n\n## General Usage\n\n````commandline\ndotcoin -h\n````\n\n````text\nusage: parity [-h] {exchanges,markets,ticker,book} ...\n\npositional arguments:\n  {exchanges,markets,ticker,book}\n    exchanges           list supported exchanges\n    markets             list supported markets\n    ticker              fetch ticker from a given market\n    book                fetch book from a given market\n\noptional arguments:\n  -h, --help            show this help message and exit\n````\n\n## Limited support\n\nAs of now, only these exchanges are supported.\n\n* BINANCE\n* BITTREX\n\nAlthough DotCoin is build on top of ccxt, which supports a considerable number of platforms, as interface which targets\nthe end-user, I consider it\'s important to provide a stable usability instead of unreliable feature set. This is why\nthere will be limited support for most exchanges in the meantime, and more will be added once certain level of\nreliability is achieved.\n\n## Thanks\n\nI greatly thank the ccxt team for their amazing work on the ccxt library, it\'s only thanks to the project they\'ve built\nthat this app is even possible. You can check their work out at their [GitHub](https://github.com/ccxt/ccxt).\n',
    'author': 'Orlando Ospino Sánchez',
    'author_email': 'oroschz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oroschz/dotcoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
