# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cfjson', 'cfjson.serde']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['python-dateutil>=2.8,<2.9']}

setup_kwargs = {
    'name': 'cf-json',
    'version': '0.1.0',
    'description': 'JSON with extensions to support serialization for common types',
    'long_description': 'cf-json\n#######\n\n**Expanded JSON serialization**\n\n.. Project Links\n\n     * `PYPI <https://https://pypi.org/project/cf-json/>`_\n     * `Documentation <https://cf-json.readthedocs.io/en/latest>`_\n     * `Gitlab <https://gitlab.clayfox.co.nz/keir/cf-json>`_\n     * `Bug Tracker <https://gitlab.clayfox.co.nz/keir/cf-json/-/issues>`_\n\n#######\n\nSummary\n-------\n\n``cf-json`` provides a batteries included approach to extending the standard `json` module.\n\n\nIt achieves this by making use of a custom `json.JSONEncoder` subclass `cfjson.MyEncoder` to\nexpand the range of types that can be serialized. While keeping sticking to the `json` interface.\n\n\nInstallation\n------------\n\nInstall the package from `PyPI <https://pypi.org/project/cf-json/>`_:\n\n.. code-block:: console\n\n    $ python -m pip install cf-json\n    [...]\n    Successfully installed cf-json\n\n\nQuick Start\n-----------\n\n`cf-json` is a drop in replacement for the standard `json` module.\n\n.. code-block:: python\n\n    >>> from cfjson import dumps, loads\n    >>> data = {1: \'a\', 2: Path(\'./my_file.py\'), 3: datetime.datetime.utcnow()}\n    >>> data\n    {1: \'a\', 2: WindowsPath(\'my_file.py\'), 3: datetime.datetime(2021, 4, 7, 2, 45, 57, 696066)}\n    >>> json_blob = dumps(data)\n    >>> json_blob\n    \'{"1": "a", "2": {"__json_type__": "WindowsPath", "path": "my_file.py"}, "3": {"__json_type__": "datetime", "datetime": "2021-04-07T02:45:57.696066"}}\'\n    >>> loads(json_blob)\n    {\'1\': \'a\', \'2\': WindowsPath(\'my_file.py\'), \'3\': datetime.datetime(2021, 4, 7, 2, 45, 57, 696066)}\n\nDocumentation\n-------------\n\n`Full documentation <https://cf-json.readthedocs.io/en/latest>`_',
    'author': 'Keir Rice',
    'author_email': 'keir@clayfox.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cf-json.readthedocs.io/en/latest/quickstart.html',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
