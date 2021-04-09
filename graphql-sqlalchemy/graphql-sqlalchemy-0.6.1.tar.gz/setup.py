# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graphql_sqlalchemy',
 'graphql_sqlalchemy.dialects',
 'graphql_sqlalchemy.dialects.pg']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.0,<2.0.0', 'graphql-core>=3.0.0,<4']

extras_require = \
{'docs': ['sphinx>=3.5.3,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<1.0.0',
          'pygments-graphql>=1.0.0,<2.0.0',
          'pygments-style-solarized>=0.1.1,<1.0.0']}

setup_kwargs = {
    'name': 'graphql-sqlalchemy',
    'version': '0.6.1',
    'description': 'Generate GraphQL Schemas from your SQLAlchemy models',
    'long_description': '# graphql-sqlalchemy\n\n[![PyPI version](https://badge.fury.io/py/graphql-sqlalchemy.svg)](https://badge.fury.io/py/graphql-sqlalchemy)\n[![Build Status](https://travis-ci.com/gzzo/graphql-sqlalchemy.svg?branch=master)](https://travis-ci.com/gzzo/graphql-sqlalchemy)\n[![codecov](https://codecov.io/gh/gzzo/graphql-sqlalchemy/branch/master/graph/badge.svg)](https://codecov.io/gh/gzzo/graphql-sqlalchemy)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nGenerate GraphQL Schemas from your SQLAlchemy models\n\n# Install\n```\npip install graphql-sqlalchemy\n```\n\n# Usage\n\n```python\n    from ariadne.asgi import GraphQL\n    from fastapi import FastAPI\n    from sqlalchemy import create_engine\n    from sqlalchemy.ext.declarative import declarative_base\n    from sqlalchemy.orm import sessionmaker\n    from graphql_sqlalchemy import build_schema\n\n    engine = create_engine(\'sqlite:///config.db\')\n    Base = declarative_base()\n    Session = sessionmaker(bind=engine)\n\n    app = FastAPI()\n    session = Session()\n\n    schema = build_schema(Base)\n\n    app.mount("/graphql", GraphQL(schema, context_value=dict(session=session)))\n```\n\n# Query\n\n```graphql\nquery {\n    user(\n        where: {\n            _or: [\n                { id: { _gte: 5 } },\n                { name: { _like: "%bob%" } },\n            ]\n        }\n    ) {\n        id\n        name\n    }\n    user_by_pk(id: 5) {\n        createtime\n    }\n}\n```\n',
    'author': 'Guido Rainuzzo',
    'author_email': 'hi@guido.nyc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gzzo/graphql-sqlalchemy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
