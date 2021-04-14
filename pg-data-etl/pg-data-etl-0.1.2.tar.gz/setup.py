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
    'version': '0.1.2',
    'description': 'ETL tools for postgres data, built on top of the psql and pg_dump command line tools',
    'long_description': '# pg-data-etl\n\nETL tools for postgres data, built on top of the psql and pg_dump command line tools.\n\n## About\n\nThis module exists to make life easier when working with geospatial data in a Postgres environment.\n\nFor example, the following code block imports a spatial table into Postgres and runs spatial queries, returned as a `geopandas.GeoDataFrame`\n\n```python\n>>> import pg_data_etl as pg\n>>> credentials = {\n...     "host": "localhost",\n...     "un": "username",\n...     "pw": "my-password",\n...     "super_un": "postgres",\n...     "super_pw": "superuser-password"\n... }\n>>> db = pg.Database("sample_database", **credentials)\n>>> db.create_db()\n>>> data_to_import = [\n...     ("philly.high_injury_network", "https://phl.carto.com/api/v2/sql?filename=high_injury_network_2020&format=geojson&skipfields=cartodb_id&q=SELECT+*+FROM+high_injury_network_2020"),\n...     ("philly.playgrounds", "https://opendata.arcgis.com/datasets/899c807e205244278b3f39421be8489c_0.geojson")\n]\n>>> for sql_tablename, source_url in data_to_import:\n...     db.import_geo_file(source_url, sql_tablename)\n>>> playground_query = """\n... select * from philly.high_injury_network\n... where st_dwithin(\n...     st_transform(geom, 26918),\n...     (select st_transform(st_collect(geom), 26918) from philly.playgrounds),\n...     100\n... )\n... order by st_length(geom) DESC """\n>>> high_injury_corridors_near_playgrounds = db.query(playground_query)\n>>> high_injury_corridors_near_playgrounds.gdf.head()\n   index  objectid            street_name   buffer                                               geom  uid\n0    234       189          BUSTLETON AVE  75 feet  LINESTRING (-75.07081 40.03528, -75.07052 40.0...  236\n1     65        38                 5TH ST  50 feet  LINESTRING (-75.14528 39.96913, -75.14502 39.9...   66\n2    223       179           ARAMINGO AVE  75 feet  LINESTRING (-75.12212 39.97449, -75.12132 39.9...  224\n3    148       215               KELLY DR  75 feet  LINESTRING (-75.18470 39.96934, -75.18513 39.9...  150\n4    156       224  MARTIN LUTHER KING DR  75 feet  LINESTRING (-75.17713 39.96327, -75.17775 39.9...  159\n```\n\nTo save time and typing, database credentials can be stored in a text file. You can place this file wherever you want,\nbut by default it\'s placed into `/USERHOME/sql_data_io/database_connections.cfg`. This file uses the following format:\n\n```\n[DEFAULT]\npw = this-is-a-placeholder-password\nport = 5432\nsuper_db = postgres\nsuper_un = postgres\nsuper_pw = this-is-another-placeholder-password\n\n[localhost]\nhost = localhost\nun = postgres\npw = your-password-here\n```\n\nEach entry in square brackets is a named connection, and any parameters not explicitly defined are inherited from `DEFAULT`.\nYou can have as many connections defined as you\'d like, and you can use them like this:\n\n```python\n>>> import pg_data_etl as pg\n>>> credentials = pg.connections()\n>>> db = pg.Database("sample_database", **credentials["localhost"])\n```\n\n## Assumptions\n\nYou should have the following command-line tools installed, preferably on your system path:\n\n- `psql`\n- `pg_dump`\n- `shp2postgis`\n- `ogr2ogr`\n\n## Installation\n\nIf you want to install into an existing environment:\n`pip install pg_data_etl`\n\nAlternatively, you can clone this repo and install an editable version:\n\n```bash\ngit clone https://github.com/aaronfraint/pg-data-etl.git\ncd pg-data-etl\npip install --editable .\n```\n\nWindows users may find the included `environment.yml` the easiest way to install, using `conda`:\n\n```bash\ngit clone https://github.com/aaronfraint/pg-data-etl.git\ncd pg-data-etl\nconda env create -f environment.yml\n```\n',
    'author': 'Aaron Fraint',
    'author_email': '38364429+aaronfraint@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aaronfraint/pg-data-etl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
