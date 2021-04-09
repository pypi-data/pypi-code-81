# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chinormfilter']

package_data = \
{'': ['*']}

install_requires = \
['sudachidict_core>=20201223.post1,<20201224',
 'sudachidict_full>=20201223.post1,<20201224',
 'sudachipy>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['chinormfilter = chinormfilter.cli:cli']}

setup_kwargs = {
    'name': 'chinormfilter',
    'version': '0.5.0',
    'description': '',
    'long_description': '# chinormfilter\n\n[![PyPi version](https://img.shields.io/pypi/v/chinormfilter.svg)](https://pypi.python.org/pypi/chinormfilter/)\n![PyTest](https://github.com/po3rin/chinormfilter/workflows/PyTest/badge.svg)\n[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-390/)\n![](https://img.shields.io/pypi/l/chinormfilter)\n\nFilter synonym files written in lucene format to avoid duplication with Sudachi normalization. Mainly used when migrating to sudachi analyzer.\n\n## Usage\n\n```sh\n$ chinormfilter tests/test.txt -o out.txt\n```\n\nfiltered result is following.\n\n```txt\nレナリドミド,レナリドマイド\nリンゴ => 林檎\n飲む,呑む\ntlc => tlc,全肺気量\nリンたんぱく質,リン蛋白質,リンタンパク質\n\n↓ filter\n\nレナリドミド,レナリドマイド\ntlc => tlc,全肺気量\n```\n\n',
    'author': 'po3rin',
    'author_email': 'abctail30@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/po3rin/chinormfilter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
