# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cans']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'cans',
    'version': '0.1.3',
    'description': 'Robust, composable, functional containers',
    'long_description': '🥫 Cans\n=======\n\n.. image:: https://img.shields.io/pypi/v/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/pypi/l/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/pypi/pyversions/cans.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/cans\n\n.. image:: https://img.shields.io/readthedocs/cans.svg?style=flat-square\n   :target: http://cans.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square\n   :target: https://github.com/psf/black\n\nSimple, functional, composable containers like ``Maybe``.\nProperly **typed** and supports **pattern matching** on Python 3.10+.\nInspired by the containers in the `Rust standard library <https://doc.rust-lang.org/std/option/>`_.\n\nQuickstart\n----------\n\n.. code-block:: python3\n\n   >>> from cans import Just, Nothing, Maybe\n   >>> greeting: Maybe[str] = Just("Hello")\n   ...\n   >>> def first(m: list[str]) -> Maybe[str]:\n   ...     return Just(m[0]) if m else Nothing()\n   ...\n   >>> first(["howdy", "hi", "hello"]).map(str.title).unwrap()\n   "Howdy"\n   ...\n   >>> # Python 3.10+ only\n   >>> match greeting:\n   ...     case Just(n):\n   ...         print(f"{greeting} world!")\n   ...     case Nothing():\n   ...         print("Hi world!")\n   Hello world!\n\nAmong the supported methods are ``flatmap``, ``filter``, ``zip``,\nas well as the relevant\n`collection APIs <https://docs.python.org/3/library/collections.abc.html>`_.\nSee `the documentation <https://cans.readthedocs.io>`_ for a complete overview.\n\nTodo\n----\n\n- Other containers\n',
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ariebovenberg/cans',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
