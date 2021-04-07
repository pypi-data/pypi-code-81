# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serialized_data_interface']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema==3.2', 'ops==1.1', 'pyyaml==5.3', 'requests==2.25']

setup_kwargs = {
    'name': 'serialized-data-interface',
    'version': '0.2.0',
    'description': 'Serialized Data Interface for Juju Operators',
    'long_description': '# Serialized Interface Library\n\nhttps://pypi.org/project/serialized-data-interface/\n\nThis libraries enables its user to create serialized and validated Juju Operator interfaces.\n\nAn interface Schema will be defined through YAML e.g:\n\n```\ntype: object\nproperties:\n  service:\n    type: string\n  port:\n    type: number\n  access-key:\n    type: string\n  secret-key:\n    type: string\n```\n\nWhen our charms interchange data, this library will validate the data through the schema on both ends.\n\n# Real World Example\n\n**** Minio with Provider Interface: https://github.com/DomFleischmann/charm-minio/tree/argo-relation\n* Argo Controller with Requirer Interface: https://github.com/DomFleischmann/argo-operators/tree/operator-v2.3.0/operators/argo-controller\n\n# TODO\n\n* Currently only provides data to App relations, should also support unit relations.\n',
    'author': 'Dominik Fleischmann',
    'author_email': 'dominik.fleischmann@canonical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/canonical/serialized-data-interface/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
