# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beanie', 'beanie.example_migration']

package_data = \
{'': ['*']}

install_requires = \
['motor>=2.1.0,<3.0.0', 'pydantic>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'beanie',
    'version': '0.3.3',
    'description': 'MongoDB ODM based on Pydantic and Motor',
    'long_description': '![Beanie](https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/with_text.svg)\n\nBeanie - is an asynchronous ODM for MongoDB, based on [Motor](https://motor.readthedocs.io/en/stable/)\nand [Pydantic](https://pydantic-docs.helpmanual.io/).\n\nIt uses an abstraction over Pydantic models and Motor collections to work with the database. Class Document allows to\ncreate, replace, update, get, find and aggregate.\n\n### Installation\n\n#### PIP\n\n```shell\npip install beanie\n```\n\n#### Poetry\n\n```shell\npoetry add beanie\n```\n\n### Quick Start\n\n**[Documentation](https://roman-right.github.io/beanie/)** - here you can find all the methods descriptions and usage examples\n\n### Resources\n\n- **[Changelog](https://roman-right.github.io/beanie/changelog)** - list of all the valuable changes\n- **[Discord](https://discord.gg/ZTTnM7rMaz)** - ask your questions, share ideas or just say `Hello!!`\n\n### Articles\n\n- [Announcing Beanie - MongoDB ODM](https://dev.to/romanright/announcing-beanie-mongodb-odm-56e)\n- [Build a Cocktail API with Beanie and MongoDB](https://developer.mongodb.com/article/beanie-odm-fastapi-cocktails/)\n- [MongoDB indexes with Beanie](https://dev.to/romanright/mongodb-indexes-with-beanie-43e8)',
    'author': 'Roman',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roman-right/beanie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
