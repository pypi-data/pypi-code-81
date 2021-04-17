# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daltonapi', 'daltonapi.tools']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'daltonapi',
    'version': '0.4.3',
    'description': 'Python wrapper for the AtomicAssets API',
    'long_description': '# Dalton\n\n![PyPI](https://img.shields.io/pypi/v/daltonapi) ![GitHub](https://img.shields.io/github/license/stuckatsixpm/dalton) [![Documentation Status](https://readthedocs.org/projects/dalton/badge/?version=latest)](https://dalton.readthedocs.io/en/latest/?badge=latest) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/06863e11a0f04b20bc45cbb920c9f3de)](https://www.codacy.com/gh/stuckatsixpm/dalton/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stuckatsixpm/dalton&amp;utm_campaign=Badge_Grade) [![CI Workflow](https://github.com/stuckatsixpm/dalton/actions/workflows/CI%20Workflow.yml/badge.svg)](https://github.com/stuckatsixpm/dalton/actions/workflows/CI%20Workflow.yml) \n\n**Note that this is an alpha release of the project, and large changes may occur, however it is intended to keep the access paths to functions and classes the same.**\n\nThis Python package provides a wrapper providing read-only access to the Atomic Assets API on the WAX blockchain. Full docs being assembled at [Read the Docs](https://dalton.readthedocs.io/en/latest/).\n\n- [Dalton](#dalton)\n  - [Features](#features)\n    - [In development](#in-development)\n  - [Installation](#installation)\n  - [Examples](#examples)\n    - [Creating an Atom object](#creating-an-atom-object)\n    - [Retrieving an asset](#retrieving-an-asset)\n    - [Retrieving assets based on criteria](#retrieving-assets-based-on-criteria)\n  - [Documentation](#documentation)\n  - [Contributing](#contributing)\n  - [Attribution](#attribution)\n  - [Contact me](#contact-me)\n\n## Features\n\n*   `Atom` class for accessing Atomic Asset Data\n*   Pythonic classes for Atomic Assets, Templates, Schemas, Collections, Transfer events, with \n*   A growing collection of class methods for working with API data.\n\n### In development\n\nHave a look at our roadmap [here](https://github.com/stuckatsixpm/dalton/projects/1).\n\n## Installation\n\nThe recommended method of installation is through PyPI and pip\n```\npython -m pip install daltonapi\n```\n*Fun fact: This package is named after John Dalton, a pioneer of Atomic Theory.*\n\n## Examples\n\n### Creating an Atom object\n\nThe main class of the Dalton package is the Atom class, which is used as an interface to the API\n``` \n>>> from daltonapi.api import Atom\n\n>>> atom = Atom()\n```\n\n### Retrieving an asset\nOnce you have created an Atom, it\'s simple to get information about an asset.\n\n``` \n>>> my_asset = atom.get_asset("1099519242825")\n>>> print(my_asset)\nAsset 1099519242825: creekdrops21 -   Bitcoin #1/21 (Max Supply: 21)\n>>>\n>>> # get link to asset\'s primary image\n>>> print(my_asset.image)\nhttps://ipfs.io/ipfs/QmUn8kvvHFrJK2mSsiPFNRMmmehnRoNJsqTP4XTVsemgrc\n>>>\n>>> # get asset collection, which is a Collection object\n>>> collection = my_asset.collection\n>>> print("Author:",collection.author)\nAuthor: creek.gm\n```\n\n### Retrieving assets based on criteria\nTo get assets based on some criteria, you can use `Atom.get_assets`, which will return a list based on criteria passed. Currently, `get_assets` accepts owner, template, schema, and/or collection as either strings or Class Objects. \n```\n>>> # Get assets using owner and template as strings\n>>> assets = atom.get_assets(owner="someowner123", template = "12345")\n>>>\n>>> # Get assets using collection class object\n>>> assets = atom.get_assets(collection=my_asset.collection)\n```\n\n## Documentation\nFull documentation is being assembled at [Read the Docs](https://dalton.readthedocs.io/en/latest/).\n\n## Contributing\nSee [Contributing](CONTRIBUTING.md).\n\nAlternatively, if you would like to sponsor me, consider donating some WAX to the address `daltonpython`.\n![https://i.imgur.com/rWbgGW3.png](https://i.imgur.com/rWbgGW3.png)\n\n## Attribution\n*   [WAX team](https://github.com/worldwide-asset-exchange) for development of the WAX blockchain.\n*   [Pink.network](https://github.com/pinknetworkx) for development of atomic assets.\n*   [PurpleBooth](https://gist.github.com/PurpleBooth) for Contributing Template.\n\n## Contact me\n*   Twitter: [@stuckat6pm](https://twitter.com/stuckat6pm)\n',
    'author': 'stuckatsixpm',
    'author_email': 'stuckat6pm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stuckatsixpm/dalton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
