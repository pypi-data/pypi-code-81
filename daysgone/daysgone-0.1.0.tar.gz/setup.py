# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daysgone']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'rich>=10.1.0,<11.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['daysgone = daysgone.main:app']}

setup_kwargs = {
    'name': 'daysgone',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Daysgone\n\nSimple typer CLI to get dates. It's based on code snippets from\n[30secondsodcode.ord](https://www.30secondsofcode.org/python/p/1) Python [date-snippets](https://www.30secondsofcode.org/python/t/date/p/1) that have been converted to use [Pendulum](https://pendulum.eustace.io/) datetime library instead of Python's built-in [datetime](https://docs.python.org/3/library/datetime.html) library.\n\n## Getting Started\n\nThese instructions will give you a copy of the project up and running on\nyour local machine for development and testing purposes. See deployment\nfor notes on deploying the project on a live system.\n\n### Prerequisites\n\nRequirements for the software and other tools to build, test and push\n- [Example 1](https://www.example.com)\n- [Example 2](https://www.example.com)\n\n### Installing\n\nA step by step series of examples that tell you how to get a development\nenvironment running\n\nSay what the step will be\n\n    Give the example\n\nAnd repeat\n\n    until finished\n\nEnd with an example of getting some data out of the system or using it\nfor a little demo\n\n## Running the tests\n\nExplain how to run the automated tests for this system\n\n### Sample Tests\n\nExplain what these tests test and why\n\n    Give an example\n\n### Style test\n\nChecks if the best practices and the right coding style has been used.\n\n    Give an example\n\n## Deployment\n\nAdd additional notes to deploy this on a live system\n\n## Built With\n\n  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used\n    for the Code of Conduct\n  - [Creative Commons](https://creativecommons.org/) - Used to choose\n    the license\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code\nof conduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [Semantic Versioning](http://semver.org/) for versioning. For the versions\navailable, see the [tags on this\nrepository](https://github.com/PurpleBooth/a-good-readme-template/tags).\n\n## Authors\n\n  - **Billie Thompson** - *Provided README Template* -\n    [PurpleBooth](https://github.com/PurpleBooth)\n\nSee also the list of\n[contributors](https://github.com/PurpleBooth/a-good-readme-template/contributors)\nwho participated in this project.\n\n## License\n\nThis project is licensed under the [CC0 1.0 Universal](LICENSE.md)\nCreative Commons License - see the [LICENSE.md](LICENSE.md) file for\ndetails\n\n## Acknowledgments\n\n  - Hat tip to anyone whose code is used\n  - Inspiration\n  - etc\n",
    'author': 'Mr.Nobody',
    'author_email': 'mrcartoonster@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
