# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envcon', 'envcon.utils']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'envcon',
    'version': '0.1.2',
    'description': '',
    'long_description': '# environs: simplified environment variable parsing\n\n\n**envcon**. easy environment variables parsing.\nenvcon allows you to store configuration separated from your code, like \n[The Twelve-Factor App](https://12factor.net/config) suggests.\n\n## Contents\n\n- [Features](#features)\n- [Install](#install)\n- [Basic usage](#basic-usage)\n- [Supported types](#supported-types)\n- [Reading .env files](#reading-env-files)\n- [Handling prefixes](#handling-prefixes)\n- [Why...?](#why)\n  - [Why environment variables?](#why-environment-variables)\n  - [Why not os.environ?](#why-not-osenviron)\n  - [Why use envcon](#why-use-envcon)\n- [License](#license)\n\n## Features\n\n- Type-casting\n- Parse `.env` files as well as environment variables (`os.environ`) (useful for development)\n- Default values\n\n## Install\n\n    pip install envcon\n\n## Basic usage\n\nAssuming these environment variables are set (or written in .env file)\n\n```bash\nexport MONGO_USER=myMongoUser\nexport MONGO_PASSWORD=shh_its_a_secret\nexport SECRET_NUMBER=0.42\nexport ONE_TO_TEN=1,2,3,4,5,6,7,8,9,10\nexport IS_ENABLED=true\nexport URL=http://www.google.com\n```\n\nParse them with envcon...\n\n```python3\nfrom envcon import environment_configuration\n\n@environment_configuration\nclass Configs:\n    SECRET_NUMBER: float\n    IS_ENABLED: bool\n    ONE_TO_TEN: list[int] # in python 3.8 use List[int] (from typing import List) \n\nprint(Configs.SECRET_NUMBER) # 0,42\nprint(type(Configs.SECRET_NUMBER)) # <class \'float\'>\nprint(Configs.IS_ENABLED) # True\nprint(type(Configs.IS_ENABLED)) # <class \'bool\'>\nprint(type(Configs.ONE_TO_TEN[0])) # <class \'int\'> \n\n@environment_configuration(prefix="MONGO_")\nclass MongoConfiguration:\n    USER: str\n    PASSWORD: str\n\nprint(MongoConfiguration.USER) # myMongoUser\n    \n```\n\n## Supported types\n\nThe following types hints are supported\n\nBuiltins and from `typing`:\n- `str`\n- `bool`\n- `int`\n- `float`\n- `list`\n- `dict` \n- `List`\n- `List[T]`\n- `Dict`\n- `Optional[T]`\n\n## Reading `.env` files\nTODO\n\n## Handling prefixes\n\n```python\nTODO\n```\n\n\nFor local development, use a `.env` file to override the default\nconfiguration.\n\n```bash\n# .env\nDEBUG=true\nSECRET_KEY="not so secret"\n```\n\n\n## Why...?\n\n### Why environment variables?\n\nSee [The 12-factor App](http://12factor.net/config) section on\n[configuration](http://12factor.net/config).\n\n### Why not `os.environ`?\n\nWhile `os.environ` is enough for simple use cases, a typical application\nwill need a way to manipulate and validate raw environment variables.\nenvirons abstracts common tasks for handling environment variables.\n\nenvirons will help you\n\n- cast environment vars to the correct type\n- specify required environment vars\n- define default values\n- parse list and dict values\n- serialize your configuration\n\n### Why use envcon?\nTODO\n\n## License\n\nMIT licensed. ',
    'author': 'Neria',
    'author_email': 'me@neria.dev',
    'maintainer': 'Neria',
    'maintainer_email': 'me@neria.dev',
    'url': 'https://github.com/neriat/envcon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
