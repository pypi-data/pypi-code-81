# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy', 'aiohttp']

setup_kwargs = {
    'name': 'aiohttp-sqlalchemy',
    'version': '0.1a2',
    'description': 'SQLAlchemy >= 1.4 support for aiohttp.',
    'long_description': "==================\naiohttp-sqlalchemy\n==================\n\nSQLAlchemy >= 1.4 support for aiohttp.\n\nInstall\n-------\n::\n\n    pip install aiohttp-sqlalchemy\n\n\nExample\n-------\n\n.. code-block:: python\n\n   from aiohttp import web\n   import aiohttp_sqlalchemy\n   from aiohttp_sqlalchemy import sa_engine, sa_middleware\n\n   routes = web.RouteTableDef()\n\n   @routes.get('/')\n   async def main(request):\n      async with request['sa_main'].begin():\n         # some code\n\n   app = web.Application(middlewares=[sa_middleware()])\n   aiohttp_sqlalchemy.setup(app, [sa_engine('sqlite+aiosqlite:///')])\n   app.add_routes(routes)\n   web.run_app(app)\n",
    'author': 'Ruslan Ilyasovich Gilfanov',
    'author_email': 'ri.gilfanov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ri-gilfanov/aiohttp-sqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
