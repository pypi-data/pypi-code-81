# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asy', 'asy.components']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'asy',
    'version': '0.0.7',
    'description': 'asy is easy and powerful supervisor for asyncio.',
    'long_description': '# asy\n[![Version](https://img.shields.io/pypi/v/asy)](https://pypi.org/project/asy)\n[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n`asy` is easy and powerful supervisor for `asyncio`.\n\n# Motivation for development\n\n- Simple cancellation\n- Improve the coordination of async functions between libraries\n- No more programs for execution management\n- Develop specifications like ASGI\n\n# Requirement\n\n- Python 3.8+\n\n# Installation\n\n``` shell\npip install asy\n```\n\n# Getting started\n\nCreate functions in `example.py`:\n\nAll you have to do is say the magic word `token`, and you can handle the function\'s lifetime at will.\n\n``` python\nimport asyncio\n\n# cancelable infinity loop\nasync def func1(token):\n    while not token.is_cancelled:\n        await asyncio.sleep(1)\n    return "complete func1."\n\n\n# uncancelable limited loop\nasync def func2(token):\n    for i in range(10):\n        await asyncio.sleep(1)\n    return f"complete func2.  result: {i}"\n\n\n# force cancel infinity loop\nasync def func3():\n    while True:\n        await asyncio.sleep(1)\n    return "complete func3. unreachable code."\n\n\n# uncancelable limited loop\ndef func4():\n    for i in range(1000):\n        ...\n    return f"complete func4.  result: {i}"\n\n# from callable\nclass YourDeamon:\n    def __init__(self, value):\n        self.value = value\n\n    async def __call__(self, token):\n        value = self.value\n\n        while not token.is_cancelled:\n            await asyncio.sleep(1)\n        return f"complete func5.  result: {value}"\n\nfunc5 = YourDeamon(1)\n\n# Do not run\n# infinity loop\n# async def func5():\n#     while True:\n#         print("waiting")\n```\n\nRun in shell.\n\n``` shell\npython3 -m asy example:func1 example:func2 example:func3 example:func4 example:func5\n```\n\nRun in Python script.\n\n``` python\nimport asy\nfrom example import func1, func2, func3, func4, func5\n\nsupervisor = asy.supervise(func1, func2, func3, func4, func5)\nsupervisor.run()\n\n# or\nasy.run(func1, func2, func3, func4, func5)\n```\n\n\nLet\'s end the daemon with `Ctrl-C` and enjoy `asy`!\n\n# Caution\n`asy` is a beta version. Please do not use it in production.\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sasano8/asy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
