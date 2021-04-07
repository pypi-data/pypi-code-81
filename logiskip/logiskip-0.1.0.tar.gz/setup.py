# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logiskip', 'logiskip.loads.roundcube']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.5,<2.0.0',
 'click-logging>=1.0.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'semantic-version>=2.8.5,<3.0.0']

extras_require = \
{'mysql': ['PyMySQL>=1.0.2,<2.0.0'], 'postgres': ['pg8000>=1.19.1,<2.0.0']}

entry_points = \
{'console_scripts': ['logiskip = logiskip.cli:logiskip'],
 'logiskip.load': ['roundcube = logiskip.loads.roundcube']}

setup_kwargs = {
    'name': 'logiskip',
    'version': '0.1.0',
    'description': 'Logical database migration between RDBMSs',
    'long_description': 'logiskip - Logical database migration between RDBMSs \n====================================================\n\nSynopsis\n--------\n\nlogiskip is a command-line tool written in Python (using `SQLAlchemy`_ that cam\nmigrate application data between different RDMSs, e.g. between MySQL and PostgreSQL.\n\nIt is modular, with the possibility to define migration logic for applications in\nseparate classes (so-called "loads").\n\nlogiskip can be used for simple tasks like mere copying of tables, but also for\nmore complex tasks (e.g. converting images to another format, converting complex\ntypes, etc.).\n\nInstallation\n------------\n\nlogiskip can be installed using `pip`. In doing so, the needed database engines\ncan be passed as extras. To install logiskip with the ability to convert between\nMySQL and PostgreSQL::\n\n  pip3 install \'logiskip[mysql,postgres]\'\n\nUsage\n-----\n\nThe package installs the `logiskip` command, which takes the following options::\n\n  --source TEXT        URI of source database\n  --destination TEXT   URI of destination database\n  --load-name TEXT     Name of load plugin for migrated application\n  --load-version TEXT  Version of migrated application/schema\n  --dry-run            Roll back transaction instead of commiting\n  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG.\n  --help               Show this message and exit.\n\nThe following example migrates an installation of `Roundcube`_ 1.4.1 from MySQL\nto PostgreSQL::\n\n  logiskip --source \'mysql://roundcube:secret@localhost/roundcube\' \\\n           --destination \'postgresql://roundcube:secret@localhost/roundcube\' \\\n\t   --load-name roundcube --load-version 1.4.1\n\nLoads\n-----\n\nLoads in logiskip define migrations for a single application within a version\nconstraint. Here is an artificial example:\n\n.. code-block:: python\n\n   from logiskip.load import BaseLoad\n   from sqlalchemy.orm import sessionmaker\n\n   class ExampleLoad(BaseLoad, name="example", version_constraint=">=1.0,<2.0"):\n       """Load for the application example within the semver contraint 1.x"""\n\n       # Table map for all migrations\n       # Tables mapped to None are skipped\n       default_tables = {\n           "cache": None  # Do not migrate the cache table\n       }\n\n       # Table map for migrating from MySQL to PostgreSQL\n       postgresql_mysql_tables = {\n           "geolocations": None,  # Application supports GIS only in PostgreSQL\n\t   "user": "users"  # Historic naming issue\n       }\n\n       # Field map for the "user" table when migrating from PostgreSQL to MySQL\n       postgresql_mysql_fields_user = {\n           "geolocation_fk": None  # See above\n       }\n\n       def mysql_postgresql_row_users(self, src_table, src_dict):\n           """Do reverse-geolocation for user addresses when migrating to PostgreSQL"""\n\t   # First, do the default conversion\n\t   dest_row = super()._convert_row_default(src_table, src_dict)\n\n\t   # Get geolocation for address\n\t   lat, lon = geocoder.reverse(dest_row["address"]\n\n\t   # Use SQLAlchemy to create a new geolocation entry\n\t   session = sessionmaker(bind=self.dest_engine)()\n\t   geoloc = self.dest_base.classes.geolocations(lat=lat, lon=lon)\n\t   session.commit()\n\n\t   # Set foreign key to geolocation\n\t   dest_row["geolocation_fk"] = geoloc.id\n\t   return dest_row\n\n       # More examples include:\n       #   x_y_field_tablename__fieldname(self, src_value) - Do a conversion on a single field value\n       #   x_y_table_tablename - Do the full table conversion manually\n       # x_y can be default in all places to be used for any migration pair\n\n\nCredits\n-------\n\nlogiskip was sponsored by:\n\n* `credativ GmbH`_\n* `Beuth Hochschule für Technik Berlin`_\n\n::\n\n   Copyright 2021 Dominik George <dominik.george@credativ.de>\n\n   Licensed under the Apache License, Version 2.0 (the "License");\n   you may not use this file except in compliance with the License.\n   You may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\n   Unless required by applicable law or agreed to in writing, software\n   distributed under the License is distributed on an "AS IS" BASIS,\n   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n   See the License for the specific language governing permissions and\n   limitations under the License.\n\n.. _SQLAlchemy: https://sqlalchemy.org/\n.. _Roundcube: https://roundcube.net/\n.. _credativ GmbH: https://credativ.de/\n.. _Beuth Hochschule für Technik Berlin: https://www.beuth-hochschule.de/\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@credativ.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/credativ/logiskip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
