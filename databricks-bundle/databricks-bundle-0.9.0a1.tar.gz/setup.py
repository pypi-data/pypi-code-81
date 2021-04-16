# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricksbundle',
 'databricksbundle.bootstrap',
 'databricksbundle.dbutils',
 'databricksbundle.notebook',
 'databricksbundle.notebook.logger',
 'databricksbundle.notebook.path',
 'databricksbundle.spark',
 'databricksbundle.spark.config',
 'databricksbundle.test']

package_data = \
{'': ['*'], 'databricksbundle': ['_config/*', '_config/databricks/*']}

install_requires = \
['console-bundle>=0.4.0,<0.5.0',
 'daipe-core>=0.8.0a1,<0.9.0',
 'injecta>=0.10.0,<0.11.0',
 'logger-bundle>=0.7.0,<0.8.0',
 'pyfony-bundles>=0.4.0,<0.5.0',
 'pyfony-core>=0.8.0,<0.9.0']

entry_points = \
{'pyfony.bundle': ['create = '
                   'databricksbundle.DatabricksBundle:DatabricksBundle.autodetect']}

setup_kwargs = {
    'name': 'databricks-bundle',
    'version': '0.9.0a1',
    'description': 'Databricks bundle for the Daipe framework',
    'long_description': '# Databricks bundle\n\nThis bundle allows you use [Daipe Framework](https://www.daipe.ai) with Databricks.  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/data-pipelines-workflow/coding-basics/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/databricks-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
