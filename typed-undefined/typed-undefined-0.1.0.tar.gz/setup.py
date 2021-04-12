# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['undefined']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'typed-undefined',
    'version': '0.1.0',
    'description': 'typed undefined',
    'long_description': '# Typed Undefined\n\nWhen `None` is not valid default value you can always use `undefined`.\n\n```python\nfrom undefined import Undefined, undefined, resolve\n\n\ndef foo(bar: Undefined[int] = undefined) -> int:\n    return resolve(undefined, 10)\n\n\nfoo(1)  # ok\nfoo(1.0)  # error\n\na: Undefined[int] = 1  # ok\nb: Undefined[int] = 0.5  # error\n```\n\n## mypy integration\n\nYou should add `undefined_mypy` to list of mypy plugins:\n\n```buildoutcfg\n[mypy]\nplugins = undefined.mypy\n```',
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/typed-undefined',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
