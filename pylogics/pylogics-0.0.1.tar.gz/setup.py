# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pylogics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylogics',
    'version': '0.0.1',
    'description': 'A Python library for logic formalisms representation and manipulation.',
    'long_description': '<h1 align="center">\n  <b>PyLogics</b>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/pylogics">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/pylogics">\n  </a>\n  <a href="https://pypi.org/project/pylogics">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pylogics" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/pylogics" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/pylogics">\n  </a>\n  <a href="">\n    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/pylogics">\n  </a>\n  <a href="https://github.com/marcofavorito/pylogics/blob/master/LICENSE">\n    <img alt="GitHub" src="https://img.shields.io/github/license/marcofavorito/pylogics">\n  </a>\n</p>\n<p align="center">\n  <a href="">\n    <img alt="test" src="https://github.com/marcofavorito/pylogics/workflows/test/badge.svg">\n  </a>\n  <a href="">\n    <img alt="lint" src="https://github.com/marcofavorito/pylogics/workflows/lint/badge.svg">\n  </a>\n  <a href="">\n    <img alt="docs" src="https://github.com/marcofavorito/pylogics/workflows/docs/badge.svg">\n  </a>\n  <a href="https://codecov.io/gh/marcofavorito/pylogics">\n    <img alt="codecov" src="https://codecov.io/gh/marcofavorito/pylogics/branch/master/graph/badge.svg?token=FG3ATGP5P5">\n  </a>\n</p>\n<p align="center">\n  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">\n    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">\n  </a>\n  <a href="https://img.shields.io/badge/mypy-checked-blue">\n    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">\n  </a>\n  <a href="https://img.shields.io/badge/code%20style-black-black">\n    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />\n  </a>\n  <a href="https://www.mkdocs.org/">\n    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">\n  </a>\n</p>\n\n\nA Python library for logic formalisms representation and manipulation.\n\n## Install\n\nTo install the package from PyPI:\n```\npip install pylogics\n```\n\n## Tests\n\nTo run tests: `tox`\n\nTo run only the code tests: `tox -e py3.7`\n\nTo run only the linters: \n- `tox -e flake8`\n- `tox -e mypy`\n- `tox -e black-check`\n- `tox -e isort-check`\n\nPlease look at the `tox.ini` file for the full list of supported commands. \n\n## Docs\n\nTo build the docs: `mkdocs build`\n\nTo view documentation in a browser: `mkdocs serve`\nand then go to [http://localhost:8000](http://localhost:8000)\n\n## License\n\npylogics is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).\n\nCopyright 2021 Marco Favorito\n\n## Authors\n\n- [Marco Favorito](https://marcofavorito.github.io/)\n',
    'author': 'MarcoFavorito',
    'author_email': 'marco.favorito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://marcofavorito.me/pylogics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
