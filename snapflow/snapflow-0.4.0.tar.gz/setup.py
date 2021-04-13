# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapflow',
 'snapflow.cli',
 'snapflow.core',
 'snapflow.core.execution',
 'snapflow.core.extraction',
 'snapflow.core.metadata',
 'snapflow.core.serialization',
 'snapflow.core.sql',
 'snapflow.core.typing',
 'snapflow.helpers',
 'snapflow.helpers.connectors',
 'snapflow.logging',
 'snapflow.migrations',
 'snapflow.migrations.versions',
 'snapflow.modules',
 'snapflow.modules.core',
 'snapflow.modules.core.snaps',
 'snapflow.project',
 'snapflow.testing',
 'snapflow.utils']

package_data = \
{'': ['*'], 'snapflow.modules.core': ['schemas/*']}

install_requires = \
['alembic>=1.5.5,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'colorful>=0.5.4,<0.6.0',
 'common-model>=0.1.1,<0.2.0',
 'datacopy>=0.1.1,<0.2.0',
 'jinja2>=2.11.1,<3.0.0',
 'loguru>=0.5.1,<0.6.0',
 'networkx>=2.4,<3.0',
 'pandas>=1.0.1,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.4.1,<2.0.0',
 'sqlparse>=0.3.1,<0.4.0',
 'strictyaml>=1.0.6,<2.0.0']

entry_points = \
{'console_scripts': ['snapflow = snapflow.cli:app']}

setup_kwargs = {
    'name': 'snapflow',
    'version': '0.4.0',
    'description': 'Functional Data Pipelines',
    'long_description': None,
    'author': 'Ken Van Haren',
    'author_email': 'kenvanharen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
