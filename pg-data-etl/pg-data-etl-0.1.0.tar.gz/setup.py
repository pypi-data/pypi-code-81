# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_data_etl', 'pg_data_etl.tests']

package_data = \
{'': ['*']}

install_requires = \
['GeoAlchemy2>=0.8.5,<0.9.0',
 'geopandas>=0.9.0,<0.10.0',
 'psycopg2>=2.8.6,<3.0.0',
 'python-dotenv>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'pg-data-etl',
    'version': '0.1.0',
    'description': 'ETL tools for postgres data, built on top of the psql and pg_dump command line tools',
    'long_description': None,
    'author': 'Aaron Fraint',
    'author_email': '38364429+aaronfraint@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
