# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_myst']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py',
 'mdformat-frontmatter>=0.3.1',
 'mdformat-tables>=0.4.0',
 'mdformat>=0.7.0,<0.8.0',
 'mdit-py-plugins>=0.2.0,<0.3.0']

entry_points = \
{'mdformat.parser_extension': ['myst = mdformat_myst.plugin']}

setup_kwargs = {
    'name': 'mdformat-myst',
    'version': '0.1.1',
    'description': 'Mdformat plugin for MyST compatibility',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-myst/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/mdformat-myst/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![PyPI version](https://img.shields.io/pypi/v/mdformat-myst)](https://pypi.org/project/mdformat-myst)\n\n# mdformat-myst\n\n> Mdformat plugin for MyST compatibility\n\n## Description\n\n[Mdformat](https://github.com/executablebooks/mdformat) is a formatter for\n[CommonMark](https://spec.commonmark.org/current/)\ncompliant Markdown.\n\nMdformat-myst is an mdformat plugin that changes the target specification to\n[MyST](https://myst-parser.readthedocs.io/en/latest/using/syntax.html),\nmaking the tool able to format the following syntax extensions:\n\n- [tables](https://github.github.com/gfm/#tables-extension-)\n- [directives](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-directives)\n  (No special handling is implemented currently.\n  Directives are parsed as if they were code fences,\n  and their content is left unchanged.)\n- [roles](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-roles)\n- [inline and block "dollar math"](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#math-shortcuts)\n- [comments](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-comments)\n- [block breaks](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-blockbreaks)\n- [targets](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-targets)\n- [front matter](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#extended-block-tokens)\n- [footnotes](https://pandoc.org/MANUAL.html#footnotes)\n\n## Install\n\n```sh\npip install mdformat-myst\n```\n\n## Usage\n\n```sh\nmdformat <filename>\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-myst',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
