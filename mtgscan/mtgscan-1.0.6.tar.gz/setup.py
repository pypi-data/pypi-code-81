# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtgscan', 'mtgscan.ocr']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'numpy==1.19.3',
 'psutil>=5.8.0,<6.0.0',
 'requests>=2.25.0,<3.0.0',
 'symspellpy>=6.7.0,<7.0.0']

setup_kwargs = {
    'name': 'mtgscan',
    'version': '1.0.6',
    'description': 'Convert an image containing Magic cards to decklist',
    'long_description': '# MTGScan\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![CodeFactor](https://www.codefactor.io/repository/github/fortierq/mtgscan/badge)](https://www.codefactor.io/repository/github/fortierq/mtgscan)\n\n![mtgscan](https://user-images.githubusercontent.com/49362475/102022934-448ffb80-3d8a-11eb-8948-3a10d190162a.jpg)\n\nMTGScan uses OCR recognition to list Magic cards from an image.  \nAfter OCR, cards are looked up in a dictionnary provided by MTGJSON (https://mtgjson.com), using fuzzy search with SymSpell (https://github.com/wolfgarbe/SymSpell).\n\nTry it online: [https://qfmtgscanapp.azurewebsites.net](https://qfmtgscanapp.azurewebsites.net/) (wait for the app to start - Azure free tier automatically shuts down the app when idle). Repository for this app: https://github.com/fortierq/mtgscan-app.\n\n## Prerequisites\n\n- Python >= 3.7\n- Credentials for the required OCR (e.g Azure Computer Vision Read API)\n\n## Installation\n\n### ... with Poetry\n\n```python\npoetry install\n```\n\n### ... with requirements\n\n```python\npip install -r requirements.txt\n```\n\n### ...  with pip\n\n```console\npip install mtgscan\n```\n\n## OCR\n\nCurrently, only Azure OCR is supported. To add an OCR, inherit mtgscan.ocr.OCR.  \n\n### Azure\n\nAPI subscription key and endpoint must be stored in environment variables `AZURE_VISION_KEY` and `AZURE_VISION_ENDPOINT` respectively.  \nSteps:\n- Subscribre for a free Azure account: https://azure.microsoft.com/free/cognitive-services\n- Create a Computer Vision resource: https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision\n- Get your key and endpoint\n\n## Tests\n\nEvery test case is stored in a separated folder in tests/samples/ containing:\n- image.*: image of Magic cards\n- deck.txt: decklist of the cards on the image\n\nTo run every test:\n```python\npoetry run python tests/test.py\n```\n\nThis produces the following outputs, for each sample and OCR:\n- statistics about number of cards found, number of errors...\n- test.log: informations about the run\n- errors.txt: history of the number of errors made by the OCR\n- box_texts.txt: output of the OCR\n\n## Basic usage\n\nLet\'s compute the decklist from the following screenshot:\n![Screenshot](https://user-images.githubusercontent.com/49362475/105632710-fa07a180-5e54-11eb-91bb-c4710ef8168f.jpeg)\n\n```python\nfrom mtgscan.text import MagicRecognition\nfrom mtgscan.ocr.azure import Azure\n\nazure = Azure()\nrec = MagicRecognition(file_all_cards="all_cards.txt", file_keywords="Keywords.json")  # download card files from mtgjson if missing\nbox_texts = azure.image_to_box_texts("https://user-images.githubusercontent.com/49362475/105632710-fa07a180-5e54-11eb-91bb-c4710ef8168f.jpeg")\ndeck = rec.box_texts_to_deck(box_texts)\nprint(deck)\n```\n\nOutput:\n```console\n4 Ancient Tomb\n4 Mishra\'s Factory\n4 Mishra\'s Workshop\n1 Strip Mine\n1 Tolarian Academy\n4 Wasteland\n1 Sacrifice\n1 Mox Ruby\n1 Mox Emerald\n1 Mox Jet\n1 Mox Pearl\n1 Mox Sapphire\n1 Black Lotus\n1 Mana Crypt\n1 Sol Ring\n4 Phyrexian Revoker\n4 Arcbound Ravager\n1 Thorn of Amethyst\n4 Sphere of Resistance\n4 Foundry Inspector\n3 Chief of the Foundry\n1 Trinisphere\n1 Lodestone Golem\n1 Mystic Forge\n2 Fleetwheel Cruiser\n1 Traxos, Scourge of Kroog\n4 Walking Ballista\n3 Stonecoil Serpent\n1 Chalice of the Void\n\n3 Mindbreak Trap\n4 Leyline of the Void\n2 Crucible of Worlds\n4 Pithing Needle\n2 Wurmcoil Engine\n```\n\n## Features\n- Tested on MTGO, Arena and IRL (simple) images\n- Handle sideboard (only on the right side)  \n- Support for stacked cards\n\n## TODO\n- Add and compare OCR (GCP, AWS...)\n- Add Twitter bot and web service\n',
    'author': 'qfortier',
    'author_email': 'qpfortier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fortierq/MTGScan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
