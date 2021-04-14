# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amqtt_db',
 'amqtt_db.base',
 'amqtt_db.db',
 'amqtt_db.payload',
 'amqtt_db.structure',
 'amqtt_db.tests',
 'amqtt_db.tests.resources',
 'amqtt_db.tests.test_db',
 'amqtt_db.tests.test_plugin']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.1,<2.0.0',
 'Sphinx>=3.5.3,<4.0.0',
 'aiounittest>=1.4.0,<2.0.0',
 'amqtt>=0.10.0-alpha.3,<0.11.0',
 'coverage>=5.5,<6.0',
 'psycopg2>=2.8.6,<3.0.0',
 'sphinx-rtd-theme>=0.5.2,<0.6.0',
 'sqlalchemy-migrate>=0.13.0,<0.14.0']

entry_points = \
{'amqtt.broker.plugins': ['amqtt_db = amqtt_db.plugin:DBPlugin']}

setup_kwargs = {
    'name': 'amqtt-db',
    'version': '0.1.2',
    'description': '',
    'long_description': 'amqtt_db\n========\n\n![license](https://img.shields.io/github/license/volkerjaenisch/amqtt_db?style=flat-square)\n![travis](https://api.travis-ci.org/volkerjaenisch/amqtt_db.svg?branch=main)\n![coverals](https://coveralls.io/repos/github/volkerjaenisch/amqtt_db/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/amqtt_db?style=flat-square)](https://pypi.org/project/amqtt/)\n[![Documantation](https://img.shields.io/readthedocs/amqtt-db.svg)](https://amqtt_db.readthedocs.io/en/latest/)\n\nDB persistence for amqtt.\n\nObjective\n---------\n\namqtt_db will persist payloads received by the [amqtt broker](https://github.com/Yakifo/amqtt) into performant relational databases.\nSQLAlchemy as well as timescaleBD are the target RMDB-Systems.\n\namqtt_db will do four steps to persist the amqtt data:\n\n 1) decoding the payload (e.G. from binary, JSON or which ever encoding)\n 1) deserializing the payload to typed Python entities\n 1) structure the session, topic, property, value information into a relational model of your choice\n 1) generate the necessary tables, columns to store the data \n\nAll of this steps can be configured via the amqtt yaml config. And you can even replace any these steps for each topic \nby your code in terms of Python plugins.\namqtt is designed to be enhanced and extended.\n\n\nPerformance\n-----------\n\nFlexibility comes with a penalty on performance. The more layers of classes and filters we \nimplement the higher the performance penalty.   \n\nSo we optimize the data flow by an optimistic approach. \n\namqtt_db expects that the decoding, deserializing, transformations, target DB, target tables, table colums \netc. are all well in place if it deals with a single incoming packet.\nIf the handling of that package fails, exceptions will be raised, and the error handling rushes in to deal with the problem.\n\nSince the change rate on the decoding, deserializing, database model is quite low this optimistic approach will be quite performant. \n\nDocumentation\n-------------\n\nPlease have a look at the [documentation](http://amqtt-db.readthedocs.io).\n',
    'author': 'volker',
    'author_email': 'volker.jaenisch@inqbus.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/volkerjaenisch/amqtt_db',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
