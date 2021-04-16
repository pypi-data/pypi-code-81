# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyquil',
 'pyquil._parser',
 'pyquil.api',
 'pyquil.experiment',
 'pyquil.external',
 'pyquil.latex',
 'pyquil.quantum_processor',
 'pyquil.quantum_processor.transformers',
 'pyquil.simulation']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.21.0,<8.0.0',
 'lark>=0.11.1,<0.12.0',
 'networkx>=2.5,<3.0',
 'numpy>=1.20,<2.0',
 'qcs-api-client>=0.7.0,<0.8.0',
 'retry>=0.9.2,<0.10.0',
 'rpcq>=3.6.0,<4.0.0',
 'scipy>=1.6.1,<2.0.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=3.5.2,<4.0.0',
                      'sphinx-rtd-theme>=0.5.1,<0.6.0',
                      'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
                      'nbsphinx>=0.8.2,<0.9.0',
                      'recommonmark>=0.7.1,<0.8.0'],
 ':python_version < "3.8"': ['importlib-metadata>=3.7.3,<4.0.0']}

setup_kwargs = {
    'name': 'pyquil',
    'version': '3.0.0rc10',
    'description': 'A Python library for creating Quantum Instruction Language (Quil) programs.',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
