# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_changelog']

package_data = \
{'': ['*'], 'auto_changelog': ['templates/*']}

install_requires = \
['Click>=7.0,<8.0',
 'docopt>=0.6.2,<0.7.0',
 'gitpython>=2.1',
 'jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['auto-changelog = auto_changelog.__main__:main']}

setup_kwargs = {
    'name': 'auto-changelog',
    'version': '0.5.3',
    'description': 'Simple tool to generate nice, formatted changelogs from vcs',
    'long_description': 'Auto Changelog\n==============\n\n|ci| |pypi| |version| |licence| |black|\n\n.. |ci| image:: https://gitlab.com/KeNaCo/auto-changelog-ci-test/badges/master/pipeline.svg\n   :target: https://gitlab.com/KeNaCo/auto-changelog-ci-test/commits/master\n   :alt: CI Pipeline\n.. |pypi| image:: https://img.shields.io/pypi/v/auto-changelog\n   :target: https://pypi.org/project/auto-changelog/\n   :alt: PyPI\n.. |version| image:: https://img.shields.io/pypi/pyversions/auto-changelog\n   :alt: PyPI - Python Version\n.. |licence| image:: https://img.shields.io/pypi/l/auto-changelog\n   :alt: PyPI - License\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :alt: Code style - Black\n\nA quick script that will generate a changelog for any git repository using `conventional style`_ commit messages.\n\nInstallation\n------------\n\nInstall and update using `pip`_:\n\n.. code-block:: text\n\n    pip install auto-changelog\n\nor directly from source(via poetry):\n\n.. code-block:: text\n\n    poetry install\n    poetry build\n    pip install dist/*.whl\n\nUsage\n-----\nYou can list the command line options by running `auto-changelog --help`:\n\n.. code-block:: text\n\n    Usage: auto-changelog [OPTIONS]\n\n    Options:\n      -p, --path-repo PATH       Path to the repository\'s root directory \n                                 [Default: .]\n\n      -t, --title TEXT           The changelog\'s title [Default: Changelog]\n      -d, --description TEXT     Your project\'s description\n      -o, --output FILENAME      The place to save the generated changelog\n                                 [Default: CHANGELOG.md]\n\n      -r, --remote TEXT          Specify git remote to use for links\n      -v, --latest-version TEXT  use specified version as latest release\n      -u, --unreleased           Include section for unreleased changes\n      --template TEXT            specify template to use [compact] or a path to a\n                                 custom template, default: compact\n\n      --diff-url TEXT            override url for compares, use {current} and\n                                 {previous} for tags\n\n      --issue-url TEXT           Override url for issues, use {id} for issue id\n      --issue-pattern TEXT       Override regex pattern for issues in commit\n                                 messages. Should contain two groups, original\n                                 match and ID used by issue-url.\n\n      --tag-pattern TEXT         override regex pattern for release tags. By\n                                 default use semver tag names semantic. tag should\n                                 be contain in one group named \'version\'.\n\n      --tag-prefix TEXT          prefix used in version tags, default: ""\n      --stdout\n      --tag-pattern TEXT         Override regex pattern for release tags\n      --starting-commit TEXT     Starting commit to use for changelog generation\n      --stopping-commit TEXT     Stopping commit to use for changelog generation\n      --debug                    set logging level to DEBUG\n      --help                     Show this message and exit.\n\n\nA simple example\n----------------\n\n.. image:: example-usage.gif\n   :alt: Example usage of auto-changelog\n\nContributing\n------------\n\nTo setup development environment, you may use `Poetry`_.\nThese instructions will assume that you have already `Poetry`_ as well as GNU make locally installed\non your development computer.\n\nThese instructions will assume that you have already poetry (https://python-poetry.org/) locally installed\non your development computer.\n\n1. Fork the `auto-changelog` repo on GitHub.\n2. Clone your fork locally::\n\n    $ git clone git@github.com:your_name_here/auto-changelog.git\n\n3. Initialize your local development environment of auto-changelog.\n   This will include creating a virtualenv using poetry, installing dependencies and registering git hooks\n   using pre-commit::\n\n    $ cd auto-changelog/\n    $ make init-dev\n\n4. Create a branch for local development::\n\n    $ git checkout -b name-of-your-bugfix-or-feature\n\n   Now you can make your changes locally.\n\n5. When you\'re done making changes, check that your changes pass linting, formating, and the\n   tests, including testing other Python versions with tox::\n\n    $ make lint         # check style with flake8\n    $ make format       # run autoformat with isort and black\n    $ make test         # run tests quickly with the default Python\n    $ make test-all     # run tests on every Python version with tox\n\n\n6. Commit your changes and push your branch to GitHub. Upon commit pre-commit will automatically run \n   flake8 and black and report if changes have been made or need to be fixed by you::\n\n    $ git add .\n    $ git commit -m "Your detailed description of your changes."\n    $ git push origin name-of-your-bugfix-or-feature\n\n7. Submit a pull request through the GitHub website.\n\n\n\n.. _Black: https://black.readthedocs.io/en/stable/\n.. _conventional style: https://www.conventionalcommits.org/en\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n.. _Poetry: https://poetry.eustace.io/\n.. _Pre-commit: https://pre-commit.com/\n',
    'author': 'Michael F Bryan',
    'author_email': 'michaelfbryan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Michael-F-Bryan/auto-changelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
