# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aries']
entry_points = \
{'console_scripts': ['aries = aries:main']}

setup_kwargs = {
    'name': 'aries-controller',
    'version': '0.7.0',
    'description': 'An unofficial telnet wrapper for "ARIES / LYNX" motor controller by Kohzu Precision Co.,Ltd.',
    'long_description': '# Python製 ARIES / LYNX モーターコントローラ ラッパー\n[![PyPI version](https://img.shields.io/pypi/v/aries_controller?style=flat-square)](https://pypi.org/project/aries_controller/#history)\n[![GitHub version](https://img.shields.io/github/v/tag/2-propanol/aries_controller?style=flat-square)](https://github.com/2-propanol/aries_controller/releases)\n[![Python Versions](https://img.shields.io/pypi/pyversions/aries_controller?style=flat-square)](https://pypi.org/project/aries_controller/)\n\n[神津精機株式会社](https://www.kohzu.co.jp/i/)さんの[ARIES / LYNX ドライバ分離型多軸モーターコントローラ](https://www.kohzu.co.jp/products/control-electronics/motor-controller-kosmos/aries-lynx/)をPythonで制御するためのラッパーです。\n研究室の4軸ステージの制御用に作成したものです。\n\n> An unofficial telnet wrapper for ["ARIES / LYNX" motor controller](https://www.kohzu.co.jp/products/control-electronics/motor-controller-kosmos/aries-lynx/) by [Kohzu Precision Co.,Ltd.](https://www.kohzu.co.jp/i/)\n> This repository is intended to work with the equipment I use in my lab. It may not work as is on equipment set up for other purposes (with different numbers and ranges of axes to operate).\n\n## Usage\n環境次第で`pip`を`pip3`や`pipenv`、`pip install`を`poetry add`や`pyflow install`などに読み替えてください。\n\n### Install\n```sh\npip install aries-controller\n```\n\n### Update\n```sh\npip install -U aries-controller\n```\n\n### `aries`(as a command line tool)\n```sh\n# aries --host <HOST> --port <PORT> <operation>\n\n# transfer raw_command(reset Z axis)\naries --raw_command ORG3/7/0\n\n# getting axis position\naries\n\n# moving axis\naries --set_position 45/90/0/-10\naries --set_position " -45/60/180/10"\n```\n> The defaults of `HOST` and `PORT` are `192.168.1.20` and `12321`.\n\n### `import`(as a Python module)\n```python\n>>> from aries import Aries\n>>> stage = Aries()\n\n>>> print(stage.position)\n(0.0, 0.0, 0.0, 0.0)\n\n>>> stage.raw_command("RPS2/4/45000/1")\n>>> print(stage.position)\n(0.0, 45.0, 0.0, 0.0)\n\n>>> stage.position[2] = 10\n<NG (TypeError)>\n>>> stage.position = [0,45,10,0]\n<OK>\n\n>>> pos = stage.position\n>>> pos[3] = 5\n>>> stage.position = pos\n<OK>\n```\n\n### Uninstall\n```sh\npip uninstall aries-controller\n```\n\n## Coordinate system\n![pan&roll](.docs/pan&roll_axis.svg)\n![tilt](.docs/tilt_axis.svg)\n![light](.docs/light_axis.svg)\n',
    'author': '2-propanol',
    'author_email': 'nuclear.fusion.247@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2-propanol/aries_controller',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
