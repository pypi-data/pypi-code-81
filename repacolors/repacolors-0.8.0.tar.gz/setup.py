# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repacolors', 'repacolors.command', 'repacolors.palette', 'repacolors.themes']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

extras_require = \
{'xextras': ['xcffib>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['repacolor = repacolors.command.repacolor:color']}

setup_kwargs = {
    'name': 'repacolors',
    'version': '0.8.0',
    'description': 'Small library for color conversion, manipulation, etc.',
    'long_description': '# repacolors\n\nSmall library for color conversion, manipulation, etc.\n\n[![Build Status](https://travis-ci.com/dyuri/repacolors.svg?branch=master)](https://travis-ci.com/dyuri/repacolors)\n\n![demo](./demo.svg)\n\n## Install\n\n```shell\n$ pip install repacolors\n```\n\nTo get the colors from `Xrdb`, install it with the `xextras` extras:\n\n```shell\n$ pip install repacolors[xextras]\n```\n\n## `repacolor` command\n\n```shell\n$ repacolor --help\nUsage: repacolor [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  adjust-contrast  Adjust the colors to match required contrast ratio.\n  colorwheel       Display colorwheel defined by `name` or created by the...\n  display          Display information about the provided colors.\n  palette          Get colors of given palette\n  pick             Pick colors from your desktop.\n  scale            Display color scale defined by the colors provided.\n```\n\n### `display`\n\nDisplay color information in the terminal.\n\n```shell\n$ repacolor display red\n\n+--------+ red - #ff0000\n|  BIG   | rgb(255, 0, 0)\n|  RED   | hsl(0, 100%, 50%)\n| SQUARE | lab(53.24% 80.09 67.2)\n+--------+\n\n$ repacolor display "#ffaad5" "rgb(128, 12, 46, .8)"\n... (displays both colors)\n$ echo "#ffffff" | repacolor display\n... (displays `white`)\n```\n\n### `pick`\n\nExecutes color picker and displays the picked color.\n\n```shell\n$ repacolor pick\n```\n\nThe integrated color picker works under _X11/linux_ if installed with *xextras*. If you want to use an external color picker, set the `COLORPICKER` environment variable:\n\n```shell\n$ export COLORPICKER=xcolor\n$ repacolor pick\n```\n\n### `palette`\n\nDisplay the colors of the palette. If no palette name provided, it shows the palettes available.\n\n```shell\n$ repacolor palette\nList of available palette names:\nryb, rybw3, orrd, pubu, ...\n\n$ repacolor palette viridis\n#440154\n#482777\n...\n```\n\n### `scale`\n\nDisplay a color scale defined by the input colors.\n\n```shell\n$ repacolor scale red white\n[colors from red to white]\n$ repacolor palette viridis | repacolor scale\n[color scale defined by `viridis` colors]\n```\n\n### `colorwheel`\n\nDisplay a color wheel.\n\nPre defined color wheels:\n\n- `ryb` - The RYB color wheel\n- `rgb` or `hsl` - The RGB color wheel\n- `lab` or `lch` - CIELAB color wheel\n\nIf no color wheel name provided, it will create one from the colors provided on `stdin`.\n\n```shell\n$ repacolor colorwheel rgb\n[RGB color wheel]\n$ repacolor scale red white black red | repacolor colorwheel\n[red - white - black color wheel]\n```\n\n### `adjust-contrast`\n\nAdjust the colors to match required contrast ratio.\n\nIf only one color is provided, chooses black or white based on the colors luminance.\n\nIf two colors are provided, tries to lighten/darken them to fulfill the contrast requirement. Starts to adjust the first color, then if it\'s not enough continues with the other.\n\nDefault contrast is 4.5 (WCAG AA). [More info on MDN.](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_WCAG/Perceivable/Color_contrast)\n\n```shell\n$ repacolor adjust-contrast red --format=lhex\n#ff0000\n#000000  # chooses black for red\n$ repacolor adjust-contrast "#555" "#5e8d87" --format=lhex\n#1d1d1d  # #555 adjusted to be darker\n#5e8d87\n$ repacolor adjust-contrast "#5e8d87" "#555" --format=lhex\n#b6cfcc  # #5e8d87 lightened\n#555555\n$ repacolor adjust-contrast "#5e8d87" "#555" -v\nColors adjusted. (2.0007 => 4.5224)\n  #5e8d87   =>   #b6cfcc\n  #555555   =>   #555555\n```\n',
    'author': 'Gyuri Horak',
    'author_email': 'dyuri@horak.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dyuri/repacolors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
