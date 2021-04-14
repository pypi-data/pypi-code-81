# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summer',
 'summer.legacy',
 'summer.legacy.flow',
 'summer.legacy.flow.base',
 'summer.legacy.model',
 'summer.legacy.model.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'networkx==2.5',
 'numba>=0.52.0,<0.53.0',
 'numpy==1.19.5',
 'scipy==1.1.0']

setup_kwargs = {
    'name': 'summerepi',
    'version': '1.1.0',
    'description': 'Summer is a compartmental disease modelling framework, written in Python. It provides a high-level API to build and run models.',
    'long_description': '# Summer: compartmental disease modelling in Python\n\n[![Automated Tests](https://github.com/monash-emu/summer/actions/workflows/tests.yml/badge.svg)](https://github.com/monash-emu/summer/actions/workflows/tests.yml)\n\nSummer is a compartmental disease modelling framework, written in Python. It provides a high-level API to build and run models. Features include:\n\n- A variety of inter-compartmental flows (infections, sojourn, fractional, births, deaths, imports)\n- Force of infection multipliers (frequency, density)\n- Post-processing of compartment sizes into derived outputs\n- Stratification of compartments, including:\n  - Adjustments to flow rates based on strata\n  - Adjustments to infectiousness based on strata\n  - Heterogeneous mixing between strata\n  - Multiple disease strains\n\nSome helpful links:\n\n- **[Documentation here](http://summerepi.com/)** with [code examples](http://summerepi.com/examples)\n- [Available on PyPi](https://pypi.org/project/summerepi/) as `summerepi`.\n- [Performance benchmarks](https://monash-emu.github.io/summer/)\n\n## Installation and Quickstart\n\nThis project is tested with Python 3.6.\nInstall the `summerepi` package from PyPI\n\n```bash\npip install summerepi\n```\n\nThen you can use the library to build and run models. See [here](http://summerepi.com/examples) for some code examples.\n\n## Performance Note\n\nYou will find a significant performance improvement in the ODE solver if you set `OMP_NUM_THREADS` before importing `summer` or `numpy`.\n\n```python\n# Set this in your Python script\nos.environ["OMP_NUM_THREADS"] = "1"\n\n# Do it before importing summer or numpy\nimport summer\n# ...\n```\n\n## Development\n\n[Poetry](https://python-poetry.org/) is used for packaging and dependency management.\n\nInitial project setup is documented [here](./docs/dev-setup.md) and should work for Windows or Ubuntu, maybe for MacOS.\n\nSome common things to do as a developer working on this codebase:\n\n```bash\n# Activate summer conda environment prior to doing other stuff (see setup docs)\nconda activate summer\n\n# Install latest requirements\npoetry install\n\n# Publish to PyPI - use your PyPI credentials\npoetry publish --build\n\n# Add a new package\npoetry add\n\n# Run tests\npytest -vv\n\n# Format Python code\nblack .\nisort . --profile black\n```\n\n## Releases\n\nReleases are numbered using [Semantic Versioning](https://semver.org/)\n\n- 1.0.0/1: Initial release\n- 1.1.0: Add stochastic integrator\n\n## Release process\n\nTo do a release:\n\n- Commit any code changes and push them to GitHub\n- Choose a new release number accoridng to [Semantic Versioning](https://semver.org/)\n- Add a release note above\n- Edit the `version` key in `pyproject.toml` to reflect the release number\n- Publish the package to [PyPI](https://pypi.org/project/summerepi/) using Poetry, you will need a PyPI login and access to the project\n- Commit the release changes and push them to GitHub (Use a commit message like "Release 1.1.0")\n\n```bash\npoetry build\npoetry publish\n```\n\npoetry publish\n\n## Documentation\n\nSphinx is used to automatically build reference documentation for this library.\nThe documentation is automatically built and deployed to [summerepi.com](http://summerepi.com/) whenever code is pushed to `master`.\n\nTo build and deploy\n\n```bash\n./docs/scripts/build.sh\n./docs/scripts/deploy.sh\n```\n\nTo work on docs locally\n\n```bash\n./docs/scripts/watch.sh\n```\n',
    'author': 'James Trauer',
    'author_email': 'james.trauer@monash.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://summerepi.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
