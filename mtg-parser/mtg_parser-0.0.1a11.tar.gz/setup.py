# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtg_parser']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pyparsing>=2.4.7,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mtg-parser',
    'version': '0.0.1a11',
    'description': 'Magic: the Gathering decklist parser',
    'long_description': '# mtg-parser\n\n\n## How to install\n\n\tpip install mtg-parser\n\n\n## How to use\n\n\timport mtg_parser\n\t\n\tdecklist = """\n\t\t1 Atraxa, Praetors\' Voice\n\t\t1 Imperial Seal\n\t\t1 Lim-Dûl\'s Vault\n\t\t1 Jeweled Lotus (CMR) 319\n\t\t1 Llanowar Elves (M12) 182\n\t\t3 Brainstorm #Card Advantage #Draw\n\t"""\n\t\n\tcards = mtg_parser.parse_deck(decklist)\n\t\n\tfor card in cards:\n\t\tprint(card[\'quantity\'], card[\'card_name\'])\n',
    'author': 'Ludovic Heyberger',
    'author_email': '940408+lheyberger@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lheyberger/mtg-parser',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
