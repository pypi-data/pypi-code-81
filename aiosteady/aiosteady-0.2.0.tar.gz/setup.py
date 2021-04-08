# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiosteady']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'attrs>=20.3.0,<21.0.0']

setup_kwargs = {
    'name': 'aiosteady',
    'version': '0.2.0',
    'description': 'Rate limiting for asyncio',
    'long_description': 'aiosteady: rate limiting for asyncio\n====================================\n\n.. image:: https://img.shields.io/pypi/v/aiosteady.svg\n        :target: https://pypi.python.org/pypi/aiosteady\n\n.. image:: https://github.com/Tinche/aiosteady/workflows/CI/badge.svg\n        :target: https://github.com/Tinche/aiosteady/actions?workflow=CI\n\n.. image:: https://codecov.io/gh/Tinche/aiosteady/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/Tinche/aiosteady\n\n.. image:: https://img.shields.io/pypi/pyversions/aiosteady.svg\n        :target: https://github.com/Tinche/aiosteady\n        :alt: Supported Python versions\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n\n----\n\n**aiosteady** is an MIT licensed library, written in Python, for rate limiting\nin asyncio applications using Redis and the aioredis_ library.\n\naiosteady currently implements the `leaky bucket algorithm`_ in a very efficient way.\n\n.. code-block:: python\n    \n    max_capacity = 10  # The bucket can contain up to 10 drops, starts with 0\n    drop_recharge = 5.0  # One drop recharges every 5 seconds.\n    throttler = Throttler(aioredis, max_capacity, drop_recharge)\n\n    # consume() returns information about success, the current bucket level,\n    # how long until the next drop recharges, etc.\n    res = await throttler.consume(f\'user:{user_id}\')\n\n.. _aioredis: https://github.com/aio-libs/aioredis\n.. _`leaky bucket algorithm`: https://en.wikipedia.org/wiki/Leaky_bucket\n\nInstallation\n------------\n\nTo install aiosteady, simply:\n\n.. code-block:: bash\n\n    $ pip install aiosteady\n\n\nUsage\n-----\n\nThe leaky bucket algorithm follows a simple model.\n\n* A single bucket contains a number of drops, called the bucket level. Buckets start with zero drops.\n* Buckets have a maximum capacity of drops.\n* Each use of the bucket (consumption) inserts one or more drops into the bucket, up until the maximum capacity. If the bucket would overflow, the consumption fails.\n* One drop leaks out every `drop_recharge` seconds, freeing space in the bucket for a new drop to be put into it.\n\n* In addition to making the consumption fail, full buckets can optionally be configured to block further attempts to consume for a period.\n\nCreate an instance of ``aiosteady.leakybucket.Throttler``, giving it an instance\nof an ``aioredis`` client and rate limiting parameters (the maximum bucket\ncapacity, the number of seconds it takes for a drop to leak out, and an\noptional blocking duration).\n\nA ``Throttler`` supports two operations: consuming and peeking.\n\n* ``await Throttler.consume("a_key")`` (``consume`` because it consumes bucket resources)\n  attempts to put the given number of drops (default 1) into the bucket at the\n  given key. It returns an instance of ``aiosteady.leakybucket.ThrottleResult``,\n  with fields for:\n\n  * ``success``: a boolean, describing whether the consumption was successful\n  * ``level``: an integer, describing the new level of the bucket\n  * ``until_next_drop``: a float, describing the number of seconds left after the next drop regenerates\n  \n  * ``blocked_for``: an optional float, if blocking is being used and the bucket is blocked, the number of seconds until the block expires\n\n* ``await Throttler.peek("a_key")`` returns the same ``ThrottleResult`` but without attempting to\n  consume any drops.\n\nBoth operations are implemented using a single Redis call, using Lua scripting.\n\nChangelog\n---------\n\n0.2.0 (2021-04-08)\n~~~~~~~~~~~~~~~~~~\n* Use the Redis ``evalsha`` instead of ``eval``, for efficiency.\n\n0.1.0 (2021-03-07)\n~~~~~~~~~~~~~~~~~~\n* Initial release.\n\nCredits\n-------\n\nThe Lua Redis script for atomic leaky bucket has been taken and heavily adapted from the Prorate_ project.\n\n.. _Prorate: https://github.com/WeTransfer/prorate\n',
    'author': 'Tin Tvrtkovic',
    'author_email': 'tinchester@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
