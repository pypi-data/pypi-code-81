# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auditless_solcx']

package_data = \
{'': ['*']}

install_requires = \
['py-solc-x>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'auditless-py-solc-x',
    'version': '0.1.0',
    'description': 'py-solc-x wrapper for Auditless',
    'long_description': '# py-solc-x wrapper for Auditless\n\nThis wrapper modifies `py-solcx-x` to produce output on every compilation so that it can be consumed by Auditless.\n\n## Can I use this for my project\n\nAs long as you are using `py-solc-x` to compile Solidity files, you can use this wrapper.\n\n## How to use\n\nAdd the the following snippet to your code:\n\n```python\nfrom pathlib import Path\nfrom auditless_solcx import solcx_start_saving_debugging_output_to_path\n\npath = Path(__file__).parent  # This will save files in a folder ./artifacts/build-info\n\nsolcx_start_saving_debugging_output_to_path(path)\n# This needs to appear before any modules consuming `py-solc-x` are loaded\n# See below "Important note about patching"\n```\n\n## Important note about patching\n\nThe patching function `solcx_start_saving_debugging_output_to_path(<path>)` needs to be called either before\n`solcx` is used directly or before any module that imports and uses `solcx`.\n\nSee [Python Mock Gotchas](https://alexmarandon.com/articles/python_mock_gotchas/) for more information about patching\norder.\n\n## License\n\nMIT\n',
    'author': 'Peteris Erins',
    'author_email': 'peteris@auditless.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/auditless/auditless-py-solc-x',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
