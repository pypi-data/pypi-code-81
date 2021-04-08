# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pidecorators']

package_data = \
{'': ['*']}

install_requires = \
['guppy3>=3.1.0,<4.0.0', 'psutil>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'pidecorators',
    'version': '0.3.0',
    'description': 'A package containing some nice decorators for buzzword bonanza functions.',
    'long_description': '# Pandora Intelligence Log decorators\nEnables users to add decorators to specific functions\n- logs\n  - log_duration\n  - log_exception\n  - log_memory\n  - log_memory_extensive\n  - log_on_end\n  - log_on_error\n  - log_on_start\n- utils\n  - copy_docstring_of\n  \n# based on \nhttps://pypi.org/project/logdecorator/ \\\nhttps://pypi.org/project/guppy3/ \\\nhttps://chase-seibert.github.io/blog/2013/08/03/diagnosing-memory-leaks-python.html \\\nhttps://github.com/pythonprofilers/memory_profiler/tree/e43d78bf6d58d5f32c1f4f4ace5b371805351eee \\\nhttps://towardsdatascience.com/using-class-decorators-in-python-2807ef52d273\n\n# additions\n- null decorators\n- tags for querying besides log level\n- store in database \n- wrap doctstrings  ',
    'author': 'David.Berenstein',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
