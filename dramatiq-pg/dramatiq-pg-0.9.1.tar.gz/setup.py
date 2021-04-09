# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dramatiq_pg']

package_data = \
{'': ['*']}

install_requires = \
['dramatiq>=1.5,<2.0', 'tenacity>=5.1.1']

entry_points = \
{'console_scripts': ['dramatiq-pg = dramatiq_pg.cli:entrypoint']}

setup_kwargs = {
    'name': 'dramatiq-pg',
    'version': '0.9.1',
    'description': 'Postgres Broker for Dramatiq Task Queue',
    'long_description': '![Dramatiq-pg](https://gitlab.com/dalibo/dramatiq-pg/raw/master/docs/logo-horizontal.png?inline=false)\n\n[Dramatiq](https://dramatiq.io/) is a simple task queue implementation for\nPython3. dramatiq-pg provides a Postgres-based implementation of a dramatiq\nbroker.\n\n\n## Features\n\n- Super simple deployment: Single table, no ORM.\n- Stores message payload and results as native JSONb.\n- Uses LISTEN/NOTIFY to keep worker sync. No polling.\n- Implements delayed task.\n- Reliable thanks to Postgres MVCC.\n- Self-healing: automatic purge of old messages. Automatic recovery after\n  crash.\n- Utility CLI for maintainance: flush, purge, stats, etc.\n\nNote that dramatiq assumes tasks are idempotent. This broker makes the same\nassumptions for recovering after a crash.\n\n\n## Installation\n\n- Install dramatiq-pg package from PyPI:\n  ``` console\n  $ pip install dramatiq-pg psycopg2-binary\n  ```\n  Ensure you have either psycopg2 or psycopg2-binary installed.\n- Init database schema with `init` command.\n  ``` console\n  $ dramatiq-pg init\n  ```\n  Or adapt `dramatiq-pg/schema.sql` to your needs.\n- Before importing actors, define global broker with a connection\n  pool:\n  ``` python\n  import dramatiq\n  import psycopg2.pool\n  from dramatiq_pg import PostgresBroker\n\n  dramatiq.set_broker(PostgresBroker(i))\n\n  @dramatiq.actor\n  def myactor():\n      ...\n  ```\n\nNow declare/import actors and manage worker just like any [dramatiq\nsetup](https://dramatiq.io/guide.html). An [example\nscript](https://gitlab.com/dalibo/dramatiq-pg/blob/master/example.py) is\navailable, tested on CI.\n\nThe CLI tool `dramatiq-pg` allows you to requeue messages, purge old messages\nand show stats on the queue. See `--help` for details.\n\n[Dramatiq-pg\ndocumentation](https://gitlab.com/dalibo/dramatiq-pg/blob/master/docs/index.rst)\nis hosted on GitLab and give you more details on deployment and operation of\nPostgres as a Dramatiq broker.\n\n\n## Integration\n\n**Django** : Use\n[django-dramatiq-pg](https://github.com/uptick/django-dramatiq-pg/) by [Curtis\nMaloney](https://gitlab.com/FunkyBob). It includes configuration, ORM model and\ndatabase migration.\n\n\n## Support\n\nIf you encounter a bug or miss a feature, please [open an issue on\nGitLab](https://gitlab.com/dalibo/dramatiq-pg/issues/new) with as much\ninformation as possible.\n\ndramatiq_pg is available under the PostgreSQL licence.\n\n\n## Credit\n\nThanks to all contributors :\n\n- Andy Freeland\n- Curtis Maloney, Django support.\n- Federico Caselli, bugfixes.\n- Giuseppe Papallo, bugfixes.\n- Rafal Kwasny, improvements.\n\n\nThe logo is a creation of [Damien CAZEILS](http://www.damiencazeils.com/)\n',
    'author': 'Étienne BERSAC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dalibo/dramatiq-pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
