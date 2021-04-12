# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['single_source']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=3.0,<4.0']}

setup_kwargs = {
    'name': 'single-source',
    'version': '0.1.5',
    'description': 'Access to the project version in Python code for PEP 621-style projects',
    'long_description': '# Single-source: There is only one truth\n> `single-source` helps to reduce the entropy in your Python project by keeping\n> single source of truth.\n\nThe targets of this library are modern Python projects which want to have\none source of truth for version, name and etc.\n\nAt the moment, the library provides the single point for a package version.\n\nIt supports Python 3.6+.\n\n## Quick start\n\n```python\n# root_package/__init__.py\nfrom pathlib import Path\nfrom single_source import get_version\n\n__version__ = get_version(__name__, Path(__file__).parent.parent)\n```\n\n## Root of the problem\n\nYou use modern `pyproject.toml` and want to keep the version of your package\nhere:\n```toml\n# pyproject.toml\n[tool.poetry]\nname = "modern-project"\nversion = "0.1.0"\n```\n\nLet\'s imagine the version of your package is required in some place of the code.\n\nSince you need the version in your Python code, you may want to duplicate the version by putting it as a string variable to some python file:\n```python\n# modern_project/__init__.py\n__version__ = "0.1.0"\n\n# modern_project/version.py\nversion = "0.1.0"\n```\n\nThen you realize you don\'t want to have the version in a python file and in pyproject.toml at the same time. It\'s harder to keep them consistent and easier to forget to bump both versions before release.\n\nAlso, you don\'t want to build the wheel by creating some script for auto incrementing the version in both places (and use it in your CI flow, for example). Instead you want use `poetry version` commands.\n\n## Installation\nYou can install `single-source` via [pip](https://pip.pypa.io/en/stable/)\n```bash\npip3 install single-source\n```\n\nor via [poetry](https://python-poetry.org/docs/#installation)\n```bash\npoetry add single-source\n```\n\nThe library also available as\n[a conda package](https://docs.conda.io/projects/conda/en/latest/) in\n[conda-forge](https://anaconda.org/conda-forge/repo) channel\n```bash\nconda install single-source --channel conda-forge\n```\n\n## Advanced usage\n### Changing default value\nIf it\'s not possible to get the version from package metadata or\nthere is no pyproject.toml `get_version` returns `""` - empty string by default.\nYou can change this value by providing a value as a `default_return` keyword argument.\n\n```python\nfrom pathlib import Path\nfrom single_source import get_version\n\npath_to_pyproject_dir = Path(__file__).parent.parent\n__version__ = get_version(__name__, path_to_pyproject_dir, default_return=None)\n```\n\n### Raising an exception\nYou may want to raise an exception in case the version of the package\nhas not been found.\n```python\nfrom pathlib import Path\nfrom single_source import get_version, VersionNotFoundError\n\npath_to_pyproject_dir = Path(__file__).parent.parent\ntry:\n    __version__ = get_version(__name__, path_to_pyproject_dir, fail=True)\nexcept VersionNotFoundError:\n    pass\n```\n\n\n### Not only pyproject.toml\nYou can use `single-source` even if you still store the version of your library\nin `setup.py` or in any other `utf-8` encoded text file.\n\n>First, try without custom `regex`, probably it can parse the version\n\nIf the default internal `regex` does not find the version in your file,\nthe only thing you need to provide is a custom `regex` to `get_version`:\n```python\nfrom single_source import get_version\n\ncustom_regex = r"\\s*version\\s*=\\s*[\\"\']\\s*([-.\\w]{3,})\\s*[\\"\']\\s*"\n\npath_to_file = "~/my-project/some_file_with_version.txt"\n__version__ = get_version(__name__, path_to_file, version_regex=custom_regex)\n```\nVersion must be in the first group `()` in the custom regex.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to\ndiscuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Daniil Shadrin',
    'author_email': 'rabbit72rus@gmail.com',
    'maintainer': 'Daniil Shadrin',
    'maintainer_email': 'rabbit72rus@gmail.com',
    'url': 'https://github.com/rabbit72/single-source',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
