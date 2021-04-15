# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['titan', 'titan.exposures', 'titan.features', 'titan.interactions']

package_data = \
{'': ['*'],
 'titan': ['params/*',
           'settings/atlanta/*',
           'settings/chicago/*',
           'settings/mississippi/*',
           'settings/nyc-msm/*',
           'settings/scott/*']}

install_requires = \
['nanoid>=2.0,<3.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.18,<2.0',
 'paraml>=0.1,<0.2']

extras_require = \
{'docs': ['mkdocs>=1.1,<2.0',
          'mkdocs-material>=7.0,<8.0',
          'mkdocstrings>=0.15.0,<0.16.0'],
 'linting': ['black>=20.8b1,<21.0', 'flake8>=3.8,<4.0', 'mypy>=0.812,<0.813']}

entry_points = \
{'console_scripts': ['run_titan = titan:script_init']}

setup_kwargs = {
    'name': 'titan-model',
    'version': '2.5.0',
    'description': 'TITAN Agent Based Model',
    'long_description': '# TITAN Simulation\n[![DOI](https://zenodo.org/badge/80315242.svg)](https://zenodo.org/badge/latestdoi/80315242)\n[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pph-collective/TITAN)](https://github.com/pph-collective/TITAN/releases/latest/) [![](https://github.com/pph-collective/TITAN/workflows/Unit%20Tests/badge.svg)](https://github.com/pph-collective/TITAN/actions) [![codecov](https://codecov.io/gh/pph-collective/TITAN/branch/develop/graph/badge.svg?token=wjkExshhyh)](https://codecov.io/gh/pph-collective/TITAN) [![GitHub](https://img.shields.io/github/license/pph-collective/TITAN)](https://github.com/pph-collective/TITAN/blob/develop/LICENSE) [![Stable](https://img.shields.io/badge/docs-stable-blue.svg)](https://pph-collective.github.io/TITAN/)\n\nTITAN (Treatment of Infectious Transmissions through Agent-based Network) is an agent-based simulation model used to explore contact transmission in complex social networks. Starting with the initializing agent population, TITAN iterates over a series of stochastic interactions where agents can interact with one another, transmit infections through various medium, and enter and exit the care continuum. The purpose of TITAN is to evaluate the impact of prevention and treatment models on incidence and prevalence rates of the targeted disease(s) through the use of data fitting simulated trajectories and rich statistics of primary/sub-population attributable proportions.\n\nAgent populations are defined as graphs (nodes connected by edges). Nodes in the graph are used to represent the attributes (or collection of attributes) of an agent (person), and edges define the type of relationship between agents. In practice, a graph represents a social network of connected people through various relationship types, and provides the medium for which agents can interact.\n\n## Getting Started\n\nInstall the package\n\n```\npip install titan-model\n```\n\nThis includes the script `run_titan` which can then be used to run the model.\n\n### Prerequisites\n\n* Python (or pypy) 3.6 or later\n\n## Running the Model\n\n```\nrun_titan -p my_params.yml\n```\n\nTo run the model, execute the `run_titan` program. See [TITAN params](https://pph-collective.github.io/titan-params-app) for documentation on how to set and use parameters.\n\nResults of the model are generated and aggregated into the `/results/` directory by default. If the model is re-run, the existing results will be overwritten.\n\n\n## Built With\n* [Python3.x](https://www.python.org/downloads/release/python-374/) - Programming language\n\n  Van Rossum G, Drake FL. Python 3 Reference Manual. Scotts Valley, CA: CreateSpace; 2009.\n\n* [Networkx](https://networkx.github.io/) - Network structure backend\n\n  Hagberg A, Swart P, S Chult D. Exploring network structure, dynamics, and function using NetworkX. 2008.\n\n* [Numpy](http://www.numpy.org/) - Numerical libraries\n\n  Oliphant TE. A guide to NumPy. Vol. 1. Trelgol Publishing USA; 2006.\n\n## Authors\n\n* **Lars Seeman** - *Initial work*\n* **Max King** - *Continued development*\n* **Sarah Bessey** - *Continued development*\n* **Mary McGrath** - *Continued development*\n\n## License\n\nThis project is licensed under the GNU General Public License version 3 - see the [LICENSE.md](LICENSE.md) file for details\n',
    'author': 'Sam Bessey',
    'author_email': 'sam_bessey@brown.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://titanmodel.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
