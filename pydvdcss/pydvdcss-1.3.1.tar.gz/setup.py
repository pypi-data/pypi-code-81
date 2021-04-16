# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydvdcss']

package_data = \
{'': ['*']}

install_requires = \
['poetry-dynamic-versioning>=0.12.4,<0.13.0']

setup_kwargs = {
    'name': 'pydvdcss',
    'version': '1.3.1',
    'description': "Python wrapper for VideoLAN's libdvdcss.",
    'long_description': "![Banner](https://rawcdn.githack.com/rlaPHOENiX/pydvdcss/dfea6bed42cf13cb9d5839ddc1c54f4efbc5ec5e/banner.png)\n\n* * *\n\n[![Docs](https://readthedocs.org/projects/pip/badge/)](https://pydvdcss.readthedocs.io)\n![Python version tests](https://github.com/rlaPHOENiX/pydvdcss/workflows/Build/badge.svg?branch=master)\n![Python versions](https://img.shields.io/pypi/pyversions/pydvdcss)\n[![PyPI version](https://img.shields.io/pypi/v/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)\n[![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)\n[![PyPI status](https://img.shields.io/pypi/status/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)\n[![GitHub issues](https://img.shields.io/github/issues/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/issues)\n[![DeepSource issues](https://deepsource.io/gh/rlaPHOENiX/pydvdcss.svg/?label=active+issues)](https://deepsource.io/gh/rlaPHOENiX/pydvdcss/?ref=repository-badge)\n[![Contributors](https://img.shields.io/github/contributors/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)\n\n**pydvdcss** is a python wrapper for VideoLAN's [libdvdcss].\n\n[libdvdcss] is a simple library designed for accessing DVDs like a block device without having to bother about the\ndecryption.\n\n  [libdvdcss]: <https://www.videolan.org/developers/libdvdcss.html>\n\n* * *\n\n## [DOCS](https://pydvdcss.readthedocs.io)\n\n## [INSTALLATION](https://pydvdcss.readthedocs.io/en/latest/installation.html)\n\n## [TO-DO](https://pydvdcss.readthedocs.io/en/latest/todo.html)\n\n* * *\n\n## [PHOENiX](https://github.com/rlaPHOENiX)\n\n## [LICENSE (GPLv3)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)\n\n## [CONTRIBUTORS](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)\n",
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': 'PHOENiX',
    'maintainer_email': 'rlaphoenix@pm.me',
    'url': 'https://github.com/rlaphoenix/pydvdcss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
