# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cutty', 'cutty.create', 'cutty.update']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.0,<8.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'packaging>=20.4,<21.0']

entry_points = \
{'console_scripts': ['cutty = cutty.__main__:main']}

setup_kwargs = {
    'name': 'cutty',
    'version': '0.1.1',
    'description': 'Cutty',
    'long_description': "Cutty\n=====\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/cutty.svg\n   :target: https://pypi.org/project/cutty/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/cutty\n   :target: https://pypi.org/project/cutty\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/cutty\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/cutty/latest.svg?label=Read%20the%20Docs\n   :target: https://cutty.readthedocs.io/\n   :alt: Read the documentation at https://cutty.readthedocs.io/\n.. |Tests| image:: https://github.com/cjolowicz/cutty/workflows/Tests/badge.svg\n   :target: https://github.com/cjolowicz/cutty/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/cjolowicz/cutty/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/cjolowicz/cutty\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Cutty* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install cutty\n\n\nUsage\n-----\n\n* TODO\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Cutty* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/cjolowicz/cutty/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/cutty',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
