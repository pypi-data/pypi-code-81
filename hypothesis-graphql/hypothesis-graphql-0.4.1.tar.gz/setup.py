# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.1.0,<4.0.0', 'hypothesis>5.8.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.4.1',
    'description': 'Hypothesis strategies for GraphQL schemas and queries',
    'long_description': 'hypothesis-graphql\n==================\n\n|Build| |Coverage| |Version| |Python versions| |Chat| |License|\n\nHypothesis strategies for GraphQL schemas, queries and data.\n\n**NOTE** This package is experimental, some features are not supported yet.\n\nUsage\n-----\n\nThere are two strategies for different use cases.\n\n1. Schema generation - ``hypothesis_graphql.strategies.schema()``\n2. Query - ``hypothesis_graphql.strategies.query(schema)``.\n\nLets take this schema as an example:\n\n.. code::\n\n    type Book {\n      title: String\n      author: Author\n    }\n\n    type Author {\n      name: String\n      books: [Book]\n    }\n\n    type Query {\n      getBooks: [Book]\n      getAuthors: [Author]\n    }\n\nThen strategies might be used in this way:\n\n.. code:: python\n\n    from hypothesis import given\n    from hypothesis_graphql import strategies as gql_st\n\n    SCHEMA = "..."  # the one above\n\n\n    @given(query=gql_st.query(SCHEMA))\n    def test_query(query):\n        ...\n        # This query might be generated:\n        #\n        # query {\n        #   getBooks {\n        #     title\n        #   }\n        # }\n\nTo restrict the set of fields in generated queries use the ``fields`` argument:\n\n.. code:: python\n\n    ...\n\n\n    @given(query=gql_st.query(SCHEMA, fields=["getAuthors"]))\n    def test_query(query):\n        # Only `getAuthors` will be generated\n        ...\n\n.. |Build| image:: https://github.com/Stranger6667/hypothesis-graphql/workflows/build/badge.svg\n   :target: https://github.com/Stranger6667/hypothesis-graphql/actions\n.. |Coverage| image:: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master\n   :alt: codecov.io status for master branch\n.. |Version| image:: https://img.shields.io/pypi/v/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |Python versions| image:: https://img.shields.io/pypi/pyversions/hypothesis-graphql.svg\n   :target: https://pypi.org/project/hypothesis-graphql/\n.. |Chat| image:: https://img.shields.io/gitter/room/Stranger6667/hypothesis-graphql.svg\n   :target: https://gitter.im/Stranger6667/hypothesis-graphql\n   :alt: Gitter\n.. |License| image:: https://img.shields.io/pypi/l/hypothesis-graphql.svg\n   :target: https://opensource.org/licenses/MIT\n',
    'author': 'Dmitry Dygalo',
    'author_email': 'dadygalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Stranger6667/hypothesis-graphql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
