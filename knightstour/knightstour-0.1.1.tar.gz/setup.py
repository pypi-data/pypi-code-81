# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['knightstour', 'knightstour.modules.knightstour']

package_data = \
{'': ['*'], 'knightstour': ['modules/*']}

setup_kwargs = {
    'name': 'knightstour',
    'version': '0.1.1',
    'description': 'A simplistic implementation of the knights tour',
    'long_description': '# Knights Tour 0.1.x\n\nA very simple implementation of the knights tour. Intended to create a lot of data work with a little bit of code.\n\n## Installation\n\nUse poetry to install package\n\n```bash\npoetry install knightstour-lucasmcgregor\n```\n\n## Usage\n\n```python\nfrom knightstour.Chessboard import Chessboard\nfrom knightstour.TourReporter import TourReporter\n\ntours = TourReporter()\nboard = Chessboard(x_size=8, y_size=8, reporter=tours)\nboard.solve_board()\n\nprint("moves checked: {0}".format(tours.moves))\nprint("we found {0} tours".format(tours.tours_count))\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Lucas McGregor',
    'author_email': 'lucasmcgregor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
