# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['svante']

package_data = \
{'': ['*']}

install_requires = \
['Pint>=0.17,<0.18',
 'attrs>=20.3.0,<21.0.0',
 'colorama>=0.4.4,<0.5.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pydove>=0.3.3,<0.4.0',
 'sciplotlib>=0.0.6,<0.0.7',
 'scipy>=1.6.2,<2.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.3.2,<0.4.0',
 'uncertainties>=3.1.5,<4.0.0']

entry_points = \
{'console_scripts': ['svante = svante.__main__:main']}

setup_kwargs = {
    'name': 'svante',
    'version': '0.0.2',
    'description': 'Configurable Arrhenius plots with uncertainties and ratios',
    'long_description': "Svante\n======\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/svante.svg\n   :target: https://pypi.org/project/svante/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/svante\n   :target: https://pypi.org/project/svante\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/svante\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/svante/latest.svg?label=Read%20the%20Docs\n   :target: https://svante.readthedocs.io/\n   :alt: Read the documentation at https://svante.readthedocs.io/\n.. |Tests| image:: https://github.com/joelb123/svante/workflows/Tests/badge.svg\n   :target: https://github.com/joelb123/svante/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/joelb123/svante/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/joelb123/svante\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Svante* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install svante\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Svante* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/joelb123/svante/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://svante.readthedocs.io/en/latest/usage.html\n",
    'author': 'Joel Berendzen',
    'author_email': 'joel@generisbio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hydrationdynamics/svante',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
