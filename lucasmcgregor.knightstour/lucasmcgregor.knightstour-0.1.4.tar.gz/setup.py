# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knightstour']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['knightstour = '
                     'lucasmcgregor.knightstour.Knightstour:main']}

setup_kwargs = {
    'name': 'lucasmcgregor.knightstour',
    'version': '0.1.4',
    'description': 'A simplistic implementation of the knights tour',
    'long_description': '# Knights Tour 0.1.x\n\nA very simple implementation of the knights tour. Intended to create a lot of data work with a little bit of code.\n\n## Installation\nUse poetry to install package\n\nTo run a tour:\n```bash\npoetry run knightstour\n```\n\n## Usage\n\n```python\nfrom lucasmcgregor.knightstour.Knightstour import Knightstour\nfrom lucasmcgregor.knightstour.TourReporter import TourReporter\n\ntours = TourReporter(logging=False)\nboard = Chessboard(x_size=8, y_size=8, reporter=tours)\nboard.solve_board()\n\nprint("moves checked: {0}".format(tours.moves))\nprint("we found {0} tours".format(tours.tours_count))\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Lucas McGregor',
    'author_email': 'lucasmcgregor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
