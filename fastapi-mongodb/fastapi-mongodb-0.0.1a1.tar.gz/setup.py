# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mongodb', 'fastapi_mongodb.tests']

package_data = \
{'': ['*']}

modules = \
['settings']
install_requires = \
['coverage',
 'faker',
 'fastapi',
 'gunicorn',
 'httpx',
 'ipython',
 'mkdocs',
 'mkdocs-material',
 'motor',
 'orjson',
 'pydantic[email,dotenv]',
 'pyjwt',
 'pymongo[tls,srv]',
 'typer',
 'uvicorn']

setup_kwargs = {
    'name': 'fastapi-mongodb',
    'version': '0.0.1a1',
    'description': 'Snippets for FastAPI to work with MongoDB by Motor driver.',
    'long_description': '![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/Kost-NavySky/fastapi_mongodb/Python%20package/master)\n![GitHub](https://img.shields.io/github/license/KosT-NavySky/fastapi_mongodb)\n[![codecov](https://codecov.io/gh/KosT-NavySky/fastapi_mongodb/branch/master/graph/badge.svg)](https://codecov.io/gh/KosT-NavySky/fastapi_mongodb)\n[![](https://img.shields.io/badge/code%20style-black-000000?style=flat)](https://github.com/psf/black)\n\n# fastapi-mongodb\n\n## Requirements\n\n- Python 3.9 +\n- poetry\n\n## Tests\n\n```\npoetry run pytest\n```\n\n## Coverage\n\n```\npoetry run coverage run -m pytest\npoetry coverage report\n```\n\n## Roadmap\n\n- ➕ BaseModel (data container and to_db / from_db)\n- ➕ BaseSchema (request / response validation and serialization)\n- ➕ BaseRepository (CRUD operations for the DB)\n- ➕ BaseRepositoryConfig (customization for Repository logic)\n- ➕ TokensHandler (encode / decode and validate JWT tokens)\n- ➕ PasswordsHandler (password hashing and password checking)\n- ➕ settings.py (get base config from .env)\n- ➕ BaseLogger (debug logger and simple logger)\n- ➕ DB profiling and monitoring\n- ➕ Application setup (config.py, indexes, collection setup)\n- ➕ Tests and test environment (test DB configuration)\n- ➕ Model Factories (factory_boy)\n- ➕➖ Pagination (?limit, ?offset, ?latest_id)\n- ➕➖ Sorting (?orderBy)\n- ➕➖ Projectors (?showFields, ?hideFields)\n- ➕➖ Trace memory allocations (tracemalloc)\n- ➕➖ BaseProfiler (decorator and context manager and metaclass / cProfile)\n- ➕➖ manage.py commands (setup apps / create apps etc)\n- ➕➖ .Dockerfile and docker-compose.yaml\n- ➕➖ DB setup (db management, db level commands)\n- ➖ DB User management commands (append to manage.py)\n- ➖ DB ReplicaSet setup + docker-compose.yaml\n- ➖ DB migrations handler (migrations running and tracking)\n- ➖ DB dump/restore\n- ➖ Filters ("Depends" classes maybe DB applicable)\n- ➖ Change email flow\n- ➖ Change password flow\n- ➖ Reset password flow\n- ➖ Load testing with Locust\n- ➖ Login with Google, Facebook, Twitter\n- ➖ .csv / .xlsx Handlers\n- ➖ Background tasks (Redis + celery/celery-beat)\n\n',
    'author': 'Kostiantyn Salnykov',
    'author_email': 'kostiantyn.salnykov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KosT-NavySky/fastapi_mongodb',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
