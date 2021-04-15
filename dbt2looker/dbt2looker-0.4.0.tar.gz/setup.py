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
    'version': '0.4.0',
    'description': 'Generate lookml view files from dbt models',
    'long_description': "# dbt2looker\n\n**Requires python >=3.7**\n\nUse `dbt2looker` to generate Looker view files automatically from dbt models.\n\n### Usage\n\nRun `dbt2looker` in the root of your dbt project:\n\n**Generate Looker view files for all models:**\n```shell\ndbt2looker\n```\n\n**Generate Looker view files for all models tagged `prod`**\n```shell\ndbt2looker --tag prod\n```\n\n## Install\n\n**Install from PyPi repository**\n\nInstall from pypi into a fresh virtual environment.\n\n```\n# Create virtual env\npython3.7 -m venv dbt2looker-venv\nsource dbt2looker-venv/bin/activate\n\n# Install\npip install dbt2looker\n\n# Run\ndbt2looker\n```\n\n**Build from source**\n\nRequires [poetry](https://python-poetry.org/docs/) and python >=3.7\n\n```\n# Install\npoetry install\n\n# Run\npoetry run dbt2looker\n```\n\n## Usage\n\n#### Generate lookml views for all dbt models in a project.\nWithin your dbt project, run:\n```\ndbt2looker\n```\nThe lookml views will be saved in:\n```\nyour_dbt_project_name/lookml\n```\n\n#### Generate lookml views for a specific set of models.\nThis is basically the same as above, except you list the specific models you're interested in. Each model name should be separated by a space:\n```\ndbt2looker olivers_cool_model kts_cooler_model\n```\n\nThe lookml views for `olivers_cool_model` and `kts_cooler_model` will be saved in:\n```\nyour_dbt_project_name/lookml\n```\n",
    'author': 'oliverlaslett',
    'author_email': 'oliver@gethubble.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hubble-data/dbt2looker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
