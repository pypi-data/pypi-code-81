# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shipmmg']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'scipy>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'shipmmg',
    'version': '0.0.6',
    'description': 'A Python package of ship maneuvering simulation',
    'long_description': "# ShipMMG: Ship Maneuvering Simulation Model\n\n[![PyPi version](https://pypip.in/v/shipmmg/badge.png)](https://pypi.org/project/shipmmg/)\n[![Anaconda-Server Badge](https://anaconda.org/taiga4112/shipmmg/badges/version.svg)](https://anaconda.org/taiga4112/shipmmg)\n![codecov](https://github.com/ShipMMG/shipmmg/workflows/codecov/badge.svg)\n[![codecov](https://codecov.io/gh/ShipMMG/shipmmg/branch/main/graph/badge.svg?token=VQ1J2RTC7X)](https://codecov.io/gh/ShipMMG/shipmmg)\n\n## What is it?\n\n**ShipMMG** is a unofficial Python package of ship maneuvering simulation with respect to the research committee on “standardization of mathematical model for ship maneuvering predictions” was organized by the JASNAOE.\n\n## Where to get it\nThe source code is currently hosted on GitHub at: [https://github.com/ShipMMG/shipmmg](https://github.com/ShipMMG/shipmmg)\n\nBinary installers for the latest released version will be available at the Python package index. Now, please install pDESy as following.\n\n```sh\npip install shipmmg\n# pip install git+ssh://git@github.com/ShipMMG/shipmmg.git # Install from GitHub\n# conda install -c conda-forge -c taiga4112 shipmmg # Install from Anaconda\n```\n\n## License\n[MIT](https://github.com/ShipMMG/shipmmg/blob/master/LICENSE)\n\n## Contribution\n1. Fork it ( http://github.com/ShipMMG/shipmmg/fork )\n2. Create your feature branch (git checkout -b my-new-feature)\n3. Commit your changes (git commit -am 'Add some feature')\n4. Push to the branch (git push origin my-new-feature)\n5. Create new Pull Request\n\nIf you want to join this project as a researcher, please contact [me](https://github.com/taiga4112).",
    'author': 'Taiga MITSUYUKI',
    'author_email': 'mitsuyuki-taiga-my@ynu.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ShipMMG/shipmmg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
