# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['immutabledict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'immutabledict',
    'version': '1.3.0',
    'description': 'Immutable wrapper around dictionaries (a fork of frozendict)',
    'long_description': '# immutabledict\n\n![PyPI](https://img.shields.io/pypi/v/immutabledict) ![Conda](https://img.shields.io/conda/vn/conda-forge/immutabledict) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/immutabledict)\n\n![License](https://img.shields.io/pypi/l/immutabledict) ![Build](https://img.shields.io/travis/com/corenting/immutabledict/master) ![Codecov](https://img.shields.io/codecov/c/github/corenting/immutabledict) ![PyPI - Downloads](https://img.shields.io/pypi/dm/immutabledict)\n\nA fork of [frozendict](https://github.com/slezica/python-frozendict), an immutable wrapper around dictionaries.\n\nIt implements the complete mapping interface and can be used as a drop-in replacement for dictionaries where immutability is desired.\nThe immutabledict constructor mimics dict, and all of the expected interfaces (iter, len, repr, hash, getitem) are provided. Note that an immutabledict does not guarantee the immutability of its values, so the utility of hash method is restricted by usage.\n\nThe only difference is that the copy() method of immutable takes variable keyword arguments, which will be present as key/value pairs in the new, immutable copy.\n\n## Installation\n\nAvailable as `immutabledict` on :\n- pypi\n- conda-forge (community-maintained, not an official release)\n\n## Example\n\n```python\nfrom immutabledict import immutabledict\n\nmy_item = immutabledict({"a": "value", "b": "other_value"})\nprint(my_item["a"]) # Print "value"\n```\n\n## Differences with frozendict\n\n- Dropped support of Python < 3.6 (version 1.0.0 supports Python 3.5)\n- Fixed `collections.Mapping` deprecation warning\n- Typing\n- [PEP 584 union operators](https://www.python.org/dev/peps/pep-0584/)\n',
    'author': 'Corentin Garcia',
    'author_email': 'corenting@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/corenting/immutabledict',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
