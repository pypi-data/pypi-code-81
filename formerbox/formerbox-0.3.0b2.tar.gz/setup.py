# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formerbox',
 'formerbox.cli',
 'formerbox.cli.functional',
 'formerbox.common',
 'formerbox.contrib',
 'formerbox.contrib.datasets',
 'formerbox.contrib.lightning',
 'formerbox.data',
 'formerbox.data.samplers',
 'formerbox.data.tokenizers',
 'formerbox.models',
 'formerbox.modules',
 'formerbox.modules.callbacks',
 'formerbox.modules.metrics',
 'formerbox.optim',
 'formerbox.tasks',
 'formerbox.tasks.code',
 'formerbox.training',
 'formerbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1.0,<6.0.0',
 'boto3>=1.17.53,<2.0.0',
 'datasets>=1.5.0,<1.6.0',
 'jsonlines>=2.0.0,<3.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'more-itertools>=8.7.0,<9.0.0',
 'numpy>=1.20.2,<2.0.0',
 'overrides_extension>=3.2.0,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pydriller>=1.15.5,<2.0.0',
 'pytorch-lightning>=1.2.0,<1.3.0',
 'sacrebleu>=1.5.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.2,<2.0.0',
 'sentencepiece>=0.1.95,<0.2.0',
 'torch>=1.8.0,<1.9.0',
 'tqdm>=4.40.0,<5.0.0',
 'traitlets>=4.3.3,<5.0.0',
 'transformers>=4.5.0,<4.6.0',
 'tree_sitter>=0.19.0,<0.20.0',
 'types-typing-extensions>=3.7.3,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'typing_inspect>=0.6.0,<0.7.0',
 'wandb>=0.10.26,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['formerbox-cli = formerbox.__main__:run_main']}

setup_kwargs = {
    'name': 'formerbox',
    'version': '0.3.0b2',
    'description': '',
    'long_description': None,
    'author': 'mozharovsky',
    'author_email': 'mozharovsky@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.4,<3.10.0',
}


setup(**setup_kwargs)
