# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonapy',
    'version': '0.1.3.dev0',
    'description': 'Library for dumping models into JSON:API',
    'long_description': '# JSON:APy - Loading and Dumping JSON:API in Python\n\n> **WIP:** this library is still in early development phase.\n\n`jsonapy` is a Python library for dumping models into\n[JSON:API-compliant]("https://jsonapi.org/") JSON.\n\n[![PyPi](https://img.shields.io/pypi/v/jsonapy?label=PyPi)](https://pypi.org/project/jsonapy/)\n[![Python Version](https://img.shields.io/pypi/pyversions/jsonapy?label=Python)](https://pypi.org/project/jsonapy/)\n![Tests & coverage](https://github.com/Arkelis/jsonapy/workflows/Tests%20&%20coverage/badge.svg)\n[![codecov](https://codecov.io/gh/Arkelis/jsonapy/branch/master/graph/badge.svg?token=ZRF5RAF8NG)](https://codecov.io/gh/Arkelis/jsonapy)\n\n## Installation\n\nWith `pip`:\n\n```\npip install jsonapy\n```\n\n## Basic usage overview\n\nThis package lets you define models and dump them into dict with the JSON:API\nstructure. First, define a resource:\n\n```python\nimport jsonapy\n\nclass PersonResource(jsonapy.BaseResource):\n    id: int\n    first_name: str\n    last_name: str\n\n    class Meta:\n        resource_name = "person"\n```\n\nYou can now dump an instance of this resource into JSON:API-structured dictionary:\n\n```python\nguido = PersonResource(id=1, first_name="Guido", last_name="Van Rossum")\ndata = guido.jsonapi_dict(required_attributes="__all__")\n```\n\nThe resulting `data` dictionary can be represented by:\n\n```python\n{\n    \'type\': \'person\',\n    \'id\': 1,\n    \'attributes\': {\n        \'firstName\': \'Guido\', \n        \'lastName\': \'Van Rossum\'\n    }\n}\n```\n\n## [Documentation](https://arkelis.github.io/jsonapy/jsonapy.html)\n\nThe complete documentation can be found **[here](https://arkelis.github.io/jsonapy/jsonapy.html)**.\nIt is built with [pdoc]("https://github.com/mitmproxy/pdoc").\n\n## [Roadmap](https://github.com/Arkelis/jsonapy/projects/1)\n\nRefer to [the project](https://github.com/Arkelis/jsonapy/projects/1) to view the roadmap-related issues.\n',
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arkelis/jsonapy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
