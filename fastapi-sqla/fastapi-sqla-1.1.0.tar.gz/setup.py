# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_sqla']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61', 'pydantic<2', 'sqlalchemy<2', 'structlog>=20']

extras_require = \
{'tests': ['alembic>=1.4.3,<2.0.0',
           'asgi_lifespan>=1.0.1,<2.0.0',
           'black>=20.8b1,<21.0',
           'Faker>=4.5.0,<5.0.0',
           'httpx>=0.15.4,<0.16.0',
           'isort>=5.5.3,<6.0.0',
           'pdbpp>=0.10.2,<0.11.0',
           'psycopg2>=2.8.6,<3.0.0',
           'pylama>=7.7.1,<8.0.0',
           'pytest>=6.0.2,<7.0.0',
           'pytest-asyncio>=0.14.0,<0.15.0',
           'pytest-cov>=2.10.1,<3.0.0',
           'pytest-watch>=4.2.0,<5.0.0',
           'tox>=3.23.0,<4.0.0']}

entry_points = \
{'pytest11': ['fastapi-sqla = fastapi_sqla._pytest_plugin']}

setup_kwargs = {
    'name': 'fastapi-sqla',
    'version': '1.1.0',
    'description': 'A highly opinionated SQLAlchemy extension for FastAPI.',
    'long_description': '# fastapi-sqla\n\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-brightgreen.svg)](https://conventionalcommits.org)\n[![CircleCI](https://circleci.com/gh/dialoguemd/fastapi-sqla.svg?style=svg&circle-token=998482f269270ee521aa54f2accbee2e22943743)](https://circleci.com/gh/dialoguemd/fastapi-sqla)\n[![codecov](https://codecov.io/gh/dialoguemd/fastapi-sqla/branch/master/graph/badge.svg?token=BQHLryClIn)](https://codecov.io/gh/dialoguemd/fastapi-sqla)\n\nA highly opinionated [SQLAlchemy] extension for [FastAPI]:\n\n* Setup using environment variables to connect on DB;\n* `fastapi_sqla.Base` a declarative base class to reflect DB tables at startup;\n* `fastapi_sqla.with_session` a dependency to get an sqla session;\n* Automated commit/rollback of sqla session at the end of request before returning\n  response;\n* Pagination utilities;\n* Pytest fixtures to easy writing test;\n\n## Configuration\n\n### Environment variables:\n\nThe keys of interest in `os.environ` are prefixed with `sqlalchemy_`.\nEach matching key (after the prefix is stripped) is treated as though it were the\ncorresponding keyword argument to [`sqlalchemy.create_engine`]\ncall.\n\nThe only required key is `sqlalchemy_url`, which provides the database URL.\n\n### Setup the app:\n\n```python\nimport fastapi_sqla\nfrom fastapi import FastAPI\n\napp = FastAPI()\nfastapi_sqla.setup(app)\n```\n\n## SQLAlchemy\n\n### Adding a new entity class:\n\n```python\nfrom fastapi_sqla import Base\n\n\nclass Entity(Base):\n    __tablename__ = "table-name-in-db"\n```\n\n### Getting an sqla session\n\n#### Using dependency injection\n\nUse [FastAPI dependency injection] to get a session as a parameter of a path operation\nfunction.\nSQLAlchemy session is committed before response is returned or rollbacked if any\nexception occurred:\n\n```python\nfrom fastapi import APIRouter, Depends\nfrom fastapi_sqla import Session\n\nrouter = APIRouter()\n\n\n@router.get("/example")\ndef example(session: Session = Depends()):\n    return session.execute("SELECT now()").scalar()\n```\n\n#### Using a context manager\n\nWhen needing a session outside of a path operation, like when using\n[FastAPI background tasks], use `fastapi_sqla.open_session` context manager.\nSQLAlchemy session is committed when exiting context or rollbacked if any exception\noccurred:\n\n```python\nfrom fastapi import APIRouter, BackgroundTasks\nfrom fastapi_sqla import open_session\n\nrouter = APIRouter()\n\n\n@router.get("/example")\ndef example(bg: BackgroundTasks):\n    bg.add_task(run_bg)\n\n\ndef run_bg():\n    with open_session() as session:\n        session.execute("SELECT now()").scalar()\n```\n\n### Pagination\n\n```python\nfrom fastapi import APIRouter, Depends\nfrom fastapi_sqla import Base, Page, Paginate\nfrom pydantic import BaseModel\nfrom sqlalchemy import select\n\nrouter = APIRouter()\n\n\nclass User(Base):\n    __tablename__ = "user"\n\n\nclass UserModel(BaseModel):\n    id: int\n    name: str\n\n\n@router.get("/users", response_model=Page[UserModel])\ndef all_users(paginate: Paginate = Depends()):\n    query = select(User)\n    return paginate(query)\n```\n\nBy default:\n\n* It returns pages of 10 items, up to 100 items;\n* Total number of items in the collection is queried using [`Query.count`]\n\n#### Customize pagination\n\nYou can customize:\n- Minimum and maximum number of items per pages;\n- How the total number of items in the collection is queried;\n\nTo customize pagination, create a dependency using `fastapi_sqla.Pagination`\n\n```python\nfrom fastapi import APIRouter, Depends\nfrom fastapi_sqla import Base, Page, Pagination, Session\nfrom pydantic import BaseModel\nfrom sqlalchemy import func, select\nfrom sqlalchemy.sql import Select\n\nrouter = APIRouter()\n\n\nclass User(Base):\n    __tablename__ = "user"\n\n\nclass UserModel(BaseModel):\n    id: int\n    name: str\n\n\ndef query_count(session: Session, query: Select) -> int:\n    return session.execute(select(func.count()).select_from(User)).scalar()\n\n\nPaginate = Pagination(\n    min_page_size=5,\n    max_page_size=500,\n    query_count=query_count,\n)\n\n\n@router.get("/users", response_model=Page[UserModel])\ndef all_users(paginate: Paginate = Depends()):\n    query = select(User)\n    return paginate(query)\n```\n\n## Pytest fixtures\n\nThis library provides a set of utility fixtures, through its PyTest plugin, which is\nautomatically installed with the library.\n\nBy default, no records are actually written to the database when running tests.\nThere currently is no way to change this behaviour.\n\n### `sqla_modules`\n\nYou must define this fixture, in order for the plugin to reflect table metadata in your\nSQLAlchemy entities. It should just import all of the application\'s modules which contain\nSQLAlchemy models.\n\nExample:\n\n```python\n# tests/conftest.py\nfrom pytest import fixture\n\n\n@fixture\ndef sqla_modules():\n    from er import sqla  # noqa\n```\n\n### `db_url`\n\nThe DB url to use.\n\nWhen `CI` key is set in environment variables, it defaults to using `postgres` as the\nhost name:\n\n```\npostgresql://postgres@posgres/postgres\n```\n\nIn other cases, the host is set to `localhost`:\n\n```\npostgresql://postgres@localhost/postgres\n```\n\nOf course, you can override it by overloading the fixture:\n\n```python\nfrom pytest import fixture\n\n\n@fixture(scope="session")\ndef db_url():\n    return "postgresql://postgres@localhost/test_database"\n```\n\n\n### `session`\n\nSqla session to create db fixture:\n* All changes done at test setup or during the test are rollbacked at test tear down;\n* No record will actually be written in the database;\n* Changes in one session need to be committed to be available from other sessions;\n\nExample:\n```python\nfrom pytest import fixture\n\n\n@fixture\ndef patient(session):\n    from er.sqla import Patient\n    patient = Patient(first_name="Bob", last_name="David")\n    session.add(patient)\n    session.commit()\n    return patient\n```\n\n### `db_migration`\n\nA session scope fixture that runs `alembic upgrade` at test session setup and\n`alembic downgrade` at tear down.\n\nIt depends on `alembic_ini_path` fixture to get the path of `alembic.ini` file.\n\nTo use in a test or test module:\n\n```python\nfrom pytest import mark\n\npytestmark = mark.usefixtures("db_migration")\n```\n\nTo use globally, add to [pytest options]:\n\n ```ini\n [pytest]\n usefixtures =\n     db_migration\n ```\n\nOr depends on it in top-level `conftest.py` and mark it as _auto-used_:\n\n```python\nfrom pytest import fixture\n\n\n@fixture(scope="session", autouse=True)\ndef db_migration(db_migration):\n    pass\n```\n\n### `alembic_ini_path`\n\nIt returns the path of  `alembic.ini` configuration file. By default, it returns\n`./alembic.ini`.\n\n\n[`sqlalchemy.create_engine`]: https://docs.sqlalchemy.org/en/13/core/engines.html?highlight=create_engine#sqlalchemy.create_engine\n[`Query.count`]: https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.count\n[pytest options]: https://docs.pytest.org/en/stable/reference.html#confval-usefixtures\n[FastAPI]: https://fastapi.tiangolo.com/\n[FastAPI dependency injection]: https://fastapi.tiangolo.com/tutorial/dependencies/\n[FastAPI background tasks]: https://fastapi.tiangolo.com/tutorial/background-tasks/\n[SQLAlchemy]: http://sqlalchemy.org/\n',
    'author': 'Hadrien David',
    'author_email': 'hadrien.david@dialogue.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dialoguemd/fastapi-sqla',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
