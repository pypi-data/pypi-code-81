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
    'version': '0.1.3',
    'description': 'Fetch an AQL directly to a Python graph representation (In NetworkX, IGraph, or Graph-Tool)',
    'long_description': "# arangodb-pythongraph\nRun an AQL and get a Python network object in return\n\n## Installation\n\n```\npip install arangodb-pythongraph\n```\nDuh.\n\n## Graph frameworks\nThis package is based on [pyintergraph](https://pypi.org/project/pyintergraph/) and thus supports extraction to NetworkX, python-IGraph and Graph-Tools graph objects.\nHowever, these libraries are not defined as requirements for this package and if you want to extract to each of them you are required to install the necessary package accordingly.\n\n\n# Usage\n\nAll queries **must** return path objects.\n\n## Simple extraction\n\n```\nfrom arangodb_pythongraph import execute_to_pygraph\n\ndb = ... # ArangoDB connection (use python-arango package)\nexample_query = '''\n  FOR v0 in vertex_collection\n    FOR e, v, p IN OUTBOUND v0 edge_collection\n      RETURN p\n'''\npython_graph = execute_to_pygraph(db, query)\nnx_graph = python_graph.to_networkx()\ngt_graph = python_graph.to_graph_tool()\nig_graph = python_graph.to_igraph()\n```\n\n## Exporting the graph\nIf you want to export the graph (for example to use it with [Gephi](https://gephi.org/)),\nyou might run into trouble if you have nested or complex attributes in your graph.\nTo overcome this, use the `cleanup` argument:\n```\npython_graph = execute_to_pygraph(db, query, cleanup=True)\n```\n\nThe functionality might be missing some use cases so if you encounter problems while exporting the graph to file,\nplease open an Issue describing the error you're getting together with a portion of the data you're trying to export.\n\n# Attaching functionality to the AQL object\nFor a neater use, run `arangodb_pythongraph.register()`\n\nBefore:\n```\npython_graph = execute_to_pythongraph(db, query)\n```\n\nAfter:\n```\npython_graph = db.aql.execute_to_pythongraph(query)\n```\n\n# Development\nContributions are more than welcome :)\n\nNote that the project is managed with [poetry](https://python-poetry.org/),\nso make sure you use poetry to update the pypoject file.\n\n## Running tests\nTo run the tests you must have a running instance of ArangoDB.\nIf you don't have a connection to an existing DB you can [use docker](https://www.arangodb.com/download-major/docker/) to run it easily.\n\nOnce you have a running ArangoDB connection, create a DB named 'test' (or any other name you choose),\nand run tests with pytest\n```\nARANGODB_PASS=<pass_goes_here> ARANGODB_NAME=test poetry run pytest\n```\n\n",
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
