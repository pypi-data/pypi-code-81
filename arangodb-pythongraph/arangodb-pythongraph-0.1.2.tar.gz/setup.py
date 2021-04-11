# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arangodb_pythongraph']

package_data = \
{'': ['*']}

install_requires = \
['pyintergraph>=1.2.0,<2.0.0', 'python-arango>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'arangodb-pythongraph',
    'version': '0.1.2',
    'description': 'Fetch an AQL directly to a Python graph representation (In NetworkX, IGraph, or Graph-Tool)',
    'long_description': "# arangodb-pythongraph\nRun an AQL and get a Python network object in return\n\n## Installation\n\n```\npip install arangodb-pythongraph\n```\nDuh.\n\n## Graph frameworks\nThis package is based on [pyintergraph](https://pypi.org/project/pyintergraph/) and thus supports extraction to NetworkX, python-IGraph and Graph-Tools graph objects.\nHowever, these libraries are not defined as requirements for this package and if you want to extract to each of them you are required to install the necessary package accordingly.\n\n\n# Usage\n\nAll queries **must** return path objects.\n\n## Simple extraction\n\n```\nfrom arangodb_pythongraph import execute_to_pygraph\n\ndb = ... # ArangoDB connection (use python-arango package)\nexample_query = '''\n  FOR v0 in vertex_collection\n    FOR e, v, p IN OUTBOUND v0 edge_collection\n      RETURN p\n'''\npython_graph = execute_to_pygraph(db, query)\nnx_graph = python_graph.to_networkx()\ngt_graph = python_graph.to_graph_tool()\nig_graph = python_graph.to_igraph()\n```\n\n# Attaching functionality to the AQL object\nFor a neater use, run `arangodb_pythongraph.register()`\n\nBefore:\n```\npython_graph = execute_to_pythongraph(db, query)\n```\n\nAfter:\n```\npython_graph = db.aql.execute_to_pythongraph(query)\n```\n\n",
    'author': 'Avi Aminov',
    'author_email': 'aviaminov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
