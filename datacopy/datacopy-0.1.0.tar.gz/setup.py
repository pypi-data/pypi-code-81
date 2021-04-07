# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datacopy',
 'datacopy.cli',
 'datacopy.data_copy',
 'datacopy.data_copy.copiers',
 'datacopy.data_copy.copiers.to_database',
 'datacopy.data_copy.copiers.to_file',
 'datacopy.data_copy.copiers.to_memory',
 'datacopy.data_copy.copiers_old',
 'datacopy.data_format',
 'datacopy.data_format.formats',
 'datacopy.data_format.formats.database',
 'datacopy.data_format.formats.file_system',
 'datacopy.data_format.formats.memory',
 'datacopy.storage',
 'datacopy.storage.database',
 'datacopy.storage.database.engines',
 'datacopy.storage.file_system',
 'datacopy.storage.file_system.engines',
 'datacopy.storage.memory',
 'datacopy.storage.memory.engines',
 'datacopy.utils']

package_data = \
{'': ['*'], 'datacopy.storage.database': ['sql_templates/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.3,<2.0.0',
 'cleo>=0.8.1,<0.9.0',
 'loguru>=0.5.3,<0.6.0',
 'networkx>=2.5,<3.0',
 'openmodel>=0.1.0,<0.2.0',
 'pandas>=1.2.3,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['snapflow = datacopy.cli:app']}

setup_kwargs = {
    'name': 'datacopy',
    'version': '0.1.0',
    'description': 'dcp - Data Copy',
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
