# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nowcastlib', 'nowcastlib.cli']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.4,<2.0', 'numpy>=1.18.5,<2.0.0', 'pandas==1.1.5']

entry_points = \
{'console_scripts': ['nowcastlib = nowcastlib.cli:main']}

setup_kwargs = {
    'name': 'nowcastlib',
    'version': '2.3.0',
    'description': '\U0001f9d9🔧 Utils that can be reused and shared across and beyond the ESO Nowcast project',
    'long_description': '# Nowcast Library\n\n\U0001f9d9\u200d♂️🔧 Utils that can be reused and shared across and beyond the ESO Nowcast\nproject\n\nThis is a public repository hosted on GitHub via a push mirror setup in the\n[internal ESO GitLab repository](https://gitlab.eso.org/gstarace/nowcastlib/)\n\n## Installation\n\nSimply run\n\n```console\npip install nowcastlib\n```\n\n## Usage and Documentation\n\nNowcast Library consists in a collection of functions organized in submodules\n(API) and a tool accessible via the command line (CLI).\n\nPlease refer to the\n[examples folder](https://github.com/thesofakillers/nowcastlib/tree/master/examples)\non GitHub for usage examples.\n\n### API\n\nHere is a quick example of how one may import nowcastlib and get access to one\nof the functions:\n\n```python\n"""Example showing how to access compute_trig_fields function"""\nimport nowcastlib as ncl\nimport pandas as pd\nimport numpy as np\n\ndata_df = pd.DataFrame(\n    [[0, 3, 4, np.NaN], [32, 4, np.NaN, 4], [56, 8, 0, np.NaN]],\n    columns=["A", "B", "C"],\n    index=pd.date_range(start="1/1/2018", periods=4, freq="2min"),\n)\n\nresult = ncl.rawdata.compute_trig_fields(data_df, ["A", "C"])\n```\n\nMore in-depth API documentation can be found\n[here](https://giuliostarace.com/nowcastlib/).\n\n### CLI\n\nSome of the library\'s functionality is bundled in configurable subcommands\naccessible via the terminal with the command `nowcastlib`:\n\n```console\nusage: nowcastlib [-h] {triangulate,chunksync} ...\n\npositional arguments:\n  {triangulate,chunksync}\n                        available commands\n    triangulate         Run `nowcastlib triangulate -h` for further help\n    chunksync           Run `nowcastlib chunksync -h` for further help\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\n## Development Setup\n\nThis repository relies on [Poetry](https://python-poetry.org/) for tracking\ndependencies, building and publishing. It is therefore recommended that\ndevelopers [install poetry](https://python-poetry.org/docs/#installation) and\nmake use of it throughout their development of the project.\n\n### Dependencies\n\nMake sure you are in the right Python environment and run\n\n```console\npoetry install\n```\n\nThis reads [pyproject.toml](./pyproject.toml), resolves the dependencies, and\ninstalls them.\n\n### Deployment\n\nThe repository is published to [PyPi](https://pypi.org/), so to make it\naccessible via a `pip install` command as mentioned [earlier](#install).\n\nTo publish changes follow these steps. Ideally this process is automated via a\nCI tool triggered by a push/merge to the master branch:\n\n1. Optionally run\n   [`poetry version`](https://python-poetry.org/docs/cli/#version) with the\n   appropriate argument based on [semver guidelines](https://semver.org/).\n\n2. Update the documentation by running\n\n   ```console\n   make document\n   ```\n\n3. Prepare the package by running\n\n   ```console\n   poetry build\n   ```\n\n4. Ensure you have [TestPyPi](https://test.pypi.org/) and PyPi configured as\n   your poetry repositories:\n\n   ```console\n   poetry config repositories.testpypi https://test.pypi.org/legacy/\n   poetry config repositories.pypi https://pypi.org/\n   ```\n\n5. Publish the repository to TestPyPi, to see that everything works as expected:\n\n   ```console\n   poetry publish -r testpypi\n   ```\n\n6. Stage, commit and push your changes (to master) with git.\n7. Publish the repository to PyPi:\n\n   ```console\n   poetry publish -r pypi\n   ```\n',
    'author': 'Giulio Starace',
    'author_email': 'giulio.starace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://giuliostarace.com/nowcastlib/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
