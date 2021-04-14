# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt2looker']

package_data = \
{'': ['*'], 'dbt2looker': ['dbt_json_schemas/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'lkml>=1.1.0,<2.0.0', 'pydantic>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['dbt2looker = dbt2looker.cli:run']}

setup_kwargs = {
    'name': 'dbt2looker',
    'version': '0.3.0',
    'description': 'Generate lookml view files from dbt models',
    'long_description': None,
    'author': 'oliverlaslett',
    'author_email': 'oliver@gethubble.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
