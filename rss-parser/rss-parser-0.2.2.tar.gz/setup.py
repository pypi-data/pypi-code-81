# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rss_parser']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1', 'lxml>=4.5.2', 'pydantic>=1.6.1', 'requests>=2.24.0']

setup_kwargs = {
    'name': 'rss-parser',
    'version': '0.2.2',
    'description': 'Typed pythonic RSS parser',
    'long_description': '# Rss parser\n\n[![Downloads](https://pepy.tech/badge/rss-parser)](https://pepy.tech/project/rss-parser)\n[![Downloads](https://pepy.tech/badge/rss-parser/month)](https://pepy.tech/project/rss-parser/month)\n[![Downloads](https://pepy.tech/badge/rss-parser/week)](https://pepy.tech/project/rss-parser/week)\n\n[![PyPI version](https://img.shields.io/pypi/v/rss-parser)](https://pypi.org/project/rss-parser)\n[![Python versions](https://img.shields.io/pypi/pyversions/rss-parser)](https://pypi.org/project/rss-parser)\n[![Wheel status](https://img.shields.io/pypi/wheel/rss-parser)](https://pypi.org/project/rss-parser)\n[![License](https://img.shields.io/pypi/l/rss-parser?color=success)](https://github.com/dhvcc/rss-parser/blob/master/LICENSE)\n[![GitHub Pages](https://badgen.net/github/status/dhvcc/rss-parser/gh-pages?label=docs)](https://dhvcc.github.io/rss-parser#documentation)\n\n[![Pypi publish](https://github.com/dhvcc/rss-parser/workflows/Pypi%20publish/badge.svg)](https://github.com/dhvcc/rss-parser/actions?query=workflow%3A%22Pypi+publish%22)\n\n# About\n\n`rss-parser` is typed python RSS parsing module built using `BeautifulSoup` and `pydantic`\n\n# Installation\n\n```bash\npip install rss-parser\n```\n\nor\n\n```bash\ngit clone https://github.com/dhvcc/rss-parser.git\ncd rss-parser\npip install .\n```\n\n# Usage\n\n```python\nfrom rss_parser import Parser\nfrom requests import get\n\nrss_url = "https://feedforall.com/sample.xml"\nxml = get(rss_url)\n\n# Limit feed output to 5 items\n# To disable limit simply do not provide the argument or use None\nparser = Parser(xml=xml.content, limit=5)\nfeed = parser.parse()\n\n# Print out feed meta data\nprint(feed.language)\nprint(feed.version)\n\n# Iteratively print feed items\nfor item in feed.feed:\n    print(item.title)\n    print(item.description)\n\n```\n\n# Contributing\n\nPull requests are welcome. For major changes, please open an issue first\nto discuss what you would like to change.\n\n# License\n\n[GPLv3](https://github.com/dhvcc/rss-parser/blob/master/LICENSE)\n',
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
