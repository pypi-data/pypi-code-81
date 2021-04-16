# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melano']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['melano = melano.cli:melano']}

setup_kwargs = {
    'name': 'melano',
    'version': '0.1.0',
    'description': 'JSON utility',
    'long_description': "# melano\n\n`melano` is JSON utility library\n\n## features\n### dict compare\n\n```shell\n>>> from melano import diff\n>>> x, y = dict(x=1, y=2), dict(x=2, z=1)\n>>> diff.compare(x, y)\n[{'field': 'x', 'x': 1, 'type': 'MISMATCH', 'y': 2, 'message': 'x: 1 (int) != 2 (int)'}, {'field': 'y', 'x': 2, 'type': 'MISSING', 'message': 'y: not found'}, {'field': 'z', 'y': 1, 'type': 'MISSING', 'message': 'z: not found'}]\n```\n\n### list of dict operations\n#### sort \n\n```shell\n>>> from melano import sort\n>>> items = [dict(x=1, y=5), dict(x=4, y=2), dict(x=2, y=3), dict(x=1, y=2)]\n>>> sort(items, 'x', 'y')\n[{'x': 1, 'y': 2}, {'x': 1, 'y': 5}, {'x': 2, 'y': 3}, {'x': 4, 'y': 2}]\n```\n\n#### group by\n\n```shell\n>>> from melano import group_by\n>>> items = [dict(x=1, y=5, z=5), dict(x=4, y=2, z=3), dict(x=4, y=2, z=10)]\n>>> group_by(items, 'x', 'y')\n[{'x': 1, 'y': 5, 'items': [{'x': 1, 'y': 5, 'z': 5}]}, {'x': 4, 'y': 2, 'items': [{'x': 4, 'y': 2, 'z': 3}, {'x': 4, 'y': 2, 'z': 10}]}]\n```\n\n#### count\n\n```shell\n>>> from melano import count\n>>> items = [dict(x=1, y=5, z=5), dict(x=4, y=2, z=3), dict(x=4, y=2, z=10)]\n>>> count(items, 'x', 'y')\n[{'x': 1, 'y': 5, 'count': 1}, {'x': 4, 'y': 2, 'count': 2}]\n```",
    'author': 'Suganthan Sundararaju',
    'author_email': 'suganthsundar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suganthsundar/melano',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
