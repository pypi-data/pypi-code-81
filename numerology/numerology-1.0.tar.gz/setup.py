# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numerology', 'numerology.pythagorean', 'numerology.pythagorean.meanings']

package_data = \
{'': ['*'],
 'numerology': ['locale/en/LC_MESSAGES/*', 'locale/fr/LC_MESSAGES/*']}

entry_points = \
{'console_scripts': ['main = main:start_app']}

setup_kwargs = {
    'name': 'numerology',
    'version': '1.0',
    'description': 'Simple numerology tool to have fun with your friends.',
    'long_description': '# Numerology\n\n## 1. About\n\nA simple numerology tool to have fun with friends.\nThe interpretations are not fully implemented yet but the mechanism to get them is fully operational.\nCurrently, you can have the life path interpretation in French and English, depending on your OS language.\n\n## 2. Installation\n\n```shell\n# Option 1: pip\npip install numerology\n\n# Option 2: Download the numerology folder on GitHub and add it to your work folder.\n```\n\n## 3. How to use it\n\n```python\n# Import\nfrom numerology import PythagoreanNumerology\n\n# Birthdate format: yyyy-mm-dd\n# Birthdate is optional to let you have a partial numerology if that information is missing.\nmy_numerology = PythagoreanNumerology("First name", "Last name", "Birthdate")\n\n# Example:\nhis_numerology = PythagoreanNumerology("Barrack", "Obama", "1961-08-04")\n```\n\nYou could chose to either get the key figures, to link it to your own interpretations, or get the available interpretations.\n\n### Get only the key figures\n\n```python\nfrom numerology import PythagoreanNumerology\nnum = Pythagorean(first_name="Barack", last_name="Obama", birthdate="1961-08-04", verbose=False)\nprint(num.key_figures)\n```\n\nThe example above should give something like this:\n\n```python\n{\n    "first_name": "Barack",\n    "last_name": "Obama",\n    "birthdate": "1961-08-04",\n    "life_path_number": 2,\n    "life_path_number_alternative": 2,\n    "hearth_desire_number": 1,\n    "personality_number": 22,\n    "destiny_number": 5,\n    "expression_number": 5,\n    "birthdate_day_num": 4,\n    "birthdate_month_num": 8,\n    "birthdate_year_num": 8,\n    "birthdate_year_num_alternative": 7,\n    "active_number": 9,\n    "legacy_number": 5,\n    "power_number": 7,\n    "power_number_alternative": 7,\n    "full_name_numbers": {\n        "1": 4,\n        "2": 3,\n        "9": 1,\n        "3": 1,\n        "6": 1,\n        "4": 1\n    },\n    "full_name_missing_numbers": [\n        5,\n        7,\n        8\n    ]\n}\n```\n\n### Get the available interpretations\n\n```python\nfrom numerology import PythagoreanNumerology\nnum = Pythagorean(first_name="Barack", last_name="Obama", birthdate="1961-08-04", verbose=False)\nprint(num.interpretations)\n```\n\nThe example above should give something like this:\n\n```python\n{\n    "first_name": "Barack",\n    "last_name": "Obama",\n    "birthdate": "1961-08-04",\n    "life_path_number": {\n        "name": "Life Path Number",\n        "number": "2",\n        "meaning": {\n            "title": "Life of collaboration and harmony with others",\n            "description": "This life path favors association and marriage. Affection and friendship are sought. It symbolizes a certain passivity and there is sometimes a tendency to live according to events. There are many twists and turns and success comes with time unless it comes unexpectedly with the help of others.\\nRequirements: The qualities needed to successfully take on this life path are: diplomacy, patience and balance.\\nChallenges: This path is difficult for those who have 2 as a missing digit, and the expression numbers 1, 5, 9, 11 and 22."\n        }\n    }\n}\n```\n\n## 4. Future log\n\nFeatures to implement:\n\n- Interpretations\n- Vedic Numerology implementation (original code by Andrii KRAVCHUK that will be adapted for consistency with the Pythagorean Numerology)\n\n## 5. Special thanks\n\nIn the beginning, this code was a simple tool for my friends who were struggling with calculations on paper. I could not imagine it would have gone so far.\n\nA special thanks to:\n\n- Stéphane Y. for the book \'ABC de la numérologie\' by Jean-Daniel FERMIER which helped me understand the world of numerology\n- Andrii KRAVCHUK (@yakninja) for transferring his ownership of the PyPi repository to me. That makes the command `pip install numerology` possible for this code\n- Kévin YAUY, PhD. (@kyauy) for letting me see all the potential of Python\n- Jennifer GORWOOD, PhD. for helping for typing the interpretations in French\n\nHave fun!\n',
    'author': 'Emmanuel GUENOU',
    'author_email': 'emmanuel@compuute.io',
    'maintainer': 'Emmanuel GUENOU',
    'maintainer_email': 'emmanuel@compuute.io',
    'url': 'https://github.com/compuuteio/numerology',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
