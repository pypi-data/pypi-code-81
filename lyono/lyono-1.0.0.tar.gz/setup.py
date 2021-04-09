# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lyono', 'lyono.clients', 'lyono.formatting']

package_data = \
{'': ['*']}

install_requires = \
['auto-all>=1.3.0,<2.0.0',
 'datamodel-code-generator>=0.6.10,<0.7.0',
 'genson>=1.2.2,<2.0.0',
 'httpx>=0.17.1,<0.18.0',
 'loguru>=0.5.3,<0.6.0',
 'orjson>=3.4.6,<4.0.0',
 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'lyono',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Hill',
    'author_email': 'kah.kevin.hill@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
