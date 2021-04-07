# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcanitexgen',
 'mcanitexgen.animation',
 'mcanitexgen.gif',
 'mcanitexgen.integration']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0', 'numpy>=1.20.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mcanitexgen = mcanitexgen.__main__:app']}

setup_kwargs = {
    'name': 'mcanitexgen',
    'version': '1.2.3',
    'description': 'An animation generator for Minecraft .mcmeta files',
    'long_description': '![](https://img.shields.io/github/license/orangeutan/mcanitexgen)\n![](https://img.shields.io/badge/python-3.8|3.9-blue)\n[![](https://img.shields.io/pypi/v/mcanitexgen)](https://pypi.org/project/mcanitexgen/)\n![](https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/6067435cfa656819bcef780415e36ff3e5f117bb/coverage.svg)\n![](https://img.shields.io/badge/mypy-checked-green)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/badge/pre--commit-enabled-green)\n![](https://github.com/orangeutan/mcanitexgen/workflows/CLI/badge.svg)\n\n# Animated-texture generator for Minecraft\nAnitexgen is a generator for ".mcmeta" files that Minecraft uses to animate textures.<br>\n\nIt allows you to write texture animations in Python instead of json. Using a proper programming language enables you to create much more complex animations, like this model that uses 3 animated textures to create a moving dog.\n\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/dog/dog.gif" width="400" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\n- [Installation](#Installation)\n- [Usage](#Usage)\n- [Getting started](#Getting-started)\n  - [Create a simple animation](#Create-a-simple-animation)\n  - [More examples](https://github.com/OrangeUtan/mcanitexgen/tree/main/examples)\n- [Changelog](https://github.com/OrangeUtan/mcanitexgen/blob/main/CHANGELOG.md)\n\n# Installation\n```\npip install mcanitexgen\n```\n\n# Usage\nGenerate .mcmeta files for all animations in an animation file\n```shell\n$ mcanitexgen generate <animation_file>\n    -o, --out       The output directory of the generated files\n    -m, --minify    Minify generated files\n    -i, --indent    Indentation used when generating files\n    --dry           Dry run. Don\'t generate any files\n```\nCreate gifs for all animations in an animation file\n```shell\n$ mcanitexgen gif <animation_file>\n    -o, --out       The output directory of the generated files\n```\n\n# Getting started\n## Create a simple animation\nWe are going to create this blinking Steve:<br>\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/steve/steve.gif" width="100" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\n\nFirst we have to create the different states of the animation.\nI created a simple **steve.png** file:<br>\n<img src="https://raw.githubusercontent.com/OrangeUtan/mcanitexgen/master/examples/steve/steve.png" width="100" style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;"/>\n\nTop to Bottom: Looking normal, blinking, wink with right eye, wink with left eye.<br>\nNow we can create the animation file **steve.animation .py** that uses these states to create an animation:<br>\n```python\nfrom mcanitexgen.animation import animation, TextureAnimation, State, Sequence\n\n@animation("steve.png")\nclass Steve(TextureAnimation):\n  NORMAL = State(0)  # Look normal\n  BLINK = State(1)\n  WINK_RIGHT = State(2)  # Wink with right eye\n  WINK_LEFT = State(3)  # Wink with left eye\n\n  # Look normal and blink shortly\n  look_and_blink = Sequence(NORMAL(duration=60), BLINK(duration=2))\n\n  # The main Sequence used to create the animation\n  main = Sequence(\n    3 * look_and_blink,  # Play "look_and_blink" Sequence 3 times\n    NORMAL(duration=60),\n    WINK_LEFT(duration=30),\n    look_and_blink,\n    NORMAL(duration=60),\n    WINK_RIGHT(duration=30),\n  )\n```\nFiles overview:\n```\nresourcepack\n  ⠇\n  textures\n    └╴ item\n       ├╴steve.png\n       └╴steve.animation.py\n```\n\nPassing the animation file to Anitexgen will create a **steve.png.mcmeta** file:\n```shell\n$ mcanitexgen generate steve.animation.py\n```\n```json\nsteve.png.mcmeta\n{\n  "animation": {\n      "interpolate": false,\n      "frametime": 1,\n      "frames": [\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 3, "time": 30},\n        {"index": 0, "time": 60},\n        {"index": 1, "time": 2},\n        {"index": 0, "time": 60},\n        {"index": 2, "time": 30}\n      ]\n  }\n}\n```\n```\nresourcepack\n  ⠇\n  textures\n    └╴ item\n       ├╴ steve.png\n       ├╴ steve.animation.py\n       └╴ steve.png.mcmeta\n```\n',
    'author': 'Oran9eUtan',
    'author_email': 'oran9eutan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangeUtan/mcanitexgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
