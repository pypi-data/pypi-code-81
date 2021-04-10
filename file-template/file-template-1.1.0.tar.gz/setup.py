# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_template']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['file-template = file_template.cli:main']}

setup_kwargs = {
    'name': 'file-template',
    'version': '1.1.0',
    'description': '',
    'long_description': '# file-template\n\n┌────────────────────────────────────────────────────┐\n│░█▀▀░▀█▀░█░░░█▀▀░░░░░▀█▀░█▀▀░█▄█░█▀█░█░░░█▀█░▀█▀░█▀▀│\n│░█▀▀░░█░░█░░░█▀▀░▄▄▄░░█░░█▀▀░█░█░█▀▀░█░░░█▀█░░█░░█▀▀│\n│░▀░░░▀▀▀░▀▀▀░▀▀▀░░░░░░▀░░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀│\n└────────────────────────────────────────────────────┘\n\nReplaces keywords in a file with the contents of another file\n\n# Installation\n\n```\npipx install file-template\n```\n\n# CLI Usage\n\n```\nUsage: file-template [OPTIONS] KEYWORD FILE1 FILE2\n\n  Replace KEYWORD in FILE1 with the contents of FILE2.\n\nOptions:\n  -i, --inplace   Edit the file in place instead of outputting to stdout.\n  -n, --no-strip  Do not strip FILE2 of leading or trailing blank characters.\n  --help          Show this message and exit.\n```\n\n# Author\n\n* Alexandre Janvrin, penetration tester at Beijaflore (https://www.beijaflore.com/en/)\n\n# License\n\nAGPLv3+, see LICENSE.txt for more details.\n\n# URLs\n\n* https://pypi.org/project/file-template/\n* https://github.com/LivinParadoX/file-template/\n',
    'author': 'Alexandre Janvrin',
    'author_email': 'alexandre.janvrin@reseau.eseo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LivinParadoX/file-template/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
