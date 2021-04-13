# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datalakebundle',
 'datalakebundle.hdfs',
 'datalakebundle.notebook',
 'datalakebundle.notebook.decorator',
 'datalakebundle.notebook.decorator.tests',
 'datalakebundle.notebook.lineage',
 'datalakebundle.notebook.lineage.argument',
 'datalakebundle.table',
 'datalakebundle.table.config',
 'datalakebundle.table.create',
 'datalakebundle.table.delete',
 'datalakebundle.table.identifier',
 'datalakebundle.table.optimize',
 'datalakebundle.table.read',
 'datalakebundle.table.schema',
 'datalakebundle.table.write',
 'datalakebundle.table.write.tests',
 'datalakebundle.test']

package_data = \
{'': ['*'], 'datalakebundle': ['_config/*']}

install_requires = \
['console-bundle>=0.4.0,<0.5.0',
 'databricks-bundle>=0.8.1b6,<0.9.0',
 'injecta>=0.10.0,<0.11.0',
 'pyfony-bundles>=0.4.0,<0.5.0',
 'simpleeval>=0.9.10,<1.0.0']

entry_points = \
{'daipe.decorator_mapping': ['input_decorators = '
                             'datalakebundle.notebook.lineage.InputDecoratorMapping:InputDecoratorMapping'],
 'pyfony.bundle': ['create = datalakebundle.DataLakeBundle:DataLakeBundle']}

setup_kwargs = {
    'name': 'datalake-bundle',
    'version': '0.6.1b3',
    'description': 'DataLake tables management bundle for the Daipe Framework',
    'long_description': '# Datalake bundle\n\nThis bundle allows you to easily create and manage datalake(house) based on the [Daipe Framework](https://www.daipe.ai).  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/data-pipelines-workflow/managing-datalake/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/datalake-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
