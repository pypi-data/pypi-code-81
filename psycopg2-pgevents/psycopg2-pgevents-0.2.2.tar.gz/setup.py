# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psycopg2_pgevents']

package_data = \
{'': ['*']}

install_requires = \
['coveralls>=2.1.1,<3.0.0',
 'psycopg2-binary>=2.7.5',
 'pytest-cov>=2.10.0,<3.0.0',
 'pytest>=5.4.3,<6.0.0']

setup_kwargs = {
    'name': 'psycopg2-pgevents',
    'version': '0.2.2',
    'description': 'PostGreSQL LISTEN/NOTIFY functionality, via psycopg2',
    'long_description': '#################\npsycopg2-pgevents\n#################\n\n.. image:: https://badge.fury.io/py/psycopg2-pgevents.svg\n    :target: https://badge.fury.io/py/psycopg2-pgevents\n.. image:: https://coveralls.io/repos/github/shawalli/psycopg2-pgevents/badge.svg?branch=master\n    :target: https://coveralls.io/github/shawalli/psycopg2-pgevents?branch=master\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n\nThis package makes it simple to use PostGreSQL\'s NOTIFY/LISTEN eventing system\nfrom Python in a consistent, pleasing manner.\n\nNote that this project officially supports Python 3.6+. This is primarily due\nto static typing.\n\n*******\nExample\n*******\n\nThe following shows an example of the package in action.\n\nAssumptions\n-----------\n\n - PostGreSQL server is running locally.\n - default database (``postgres``) is available.\n - table exists in database in the public schema with the name ``orders``.\n\n.. code-block:: python\n\n    from psycopg2 import connect\n    from psycopg2_pgevents.trigger import install_trigger, \\\n        install_trigger_function, uninstall_trigger, uninstall_trigger_function\n    from psycopg2_pgevents.event import poll, register_event_channel, \\\n        unregister_event_channel\n\n    connection = connect(dsn=\'postgres:///postgres\')\n    connection.autocommit = True\n\n    install_trigger_function(connection)\n    install_trigger(connection, \'orders\')\n    register_event_channel(connection)\n\n    try:\n        print(\'Listening for events...\')\n        while True:\n            for evt in poll(connection):\n                print(\'New Event: {}\'.format(evt))\n    except KeyboardInterrupt:\n        print(\'User exit via Ctrl-C; Shutting down...\')\n        unregister_event_channel(connection)\n        uninstall_trigger(connection, \'orders\')\n        uninstall_trigger_function(connection)\n        print(\'Shutdown complete.\')\n\n***************\nTroubleshooting\n***************\n\n* The connection\'s ``autocommit`` property must be enabled for this package to\n  operate correctly. This requirement is provided by PostGreSQL\'s NOTIFY/LISTEN\n  mechanism.\n\n* The same connection that is used with ``register_event_channel()`` must be\n  used with ``poll()`` in order to receive events. This is due to the nature of\n  how PostGreSQL manages "listening" connections.\n\n* If the table that you\'d like to listen to is not in the public schema, the\n  schema name must be given as a keyword argument in the ``install_trigger()``\n  method.\n\n**********************\nAuthorship and License\n**********************\n\nWritten by Shawn Wallis and distributed under the MIT license.\n',
    'author': 'Shawn Wallis',
    'author_email': 'shawn.p.wallis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shawalli/psycopg2-pgevents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
