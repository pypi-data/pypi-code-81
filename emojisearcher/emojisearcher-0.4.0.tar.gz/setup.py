# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emojisearcher']

package_data = \
{'': ['*']}

install_requires = \
['emoji>=1.2.0,<2.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['emo = emojisearcher.script:main']}

setup_kwargs = {
    'name': 'emojisearcher',
    'version': '0.4.0',
    'description': 'Look up emojis by text and copy them to the clipboard.',
    'long_description': '## Emoji Searcher\n\nAutomate the boring stuff: I have been googling emojis and manually copying them to my clipboard.\n\nSo it was time to write a script to look up emojis by text from the command line and copy them to the clipboard.\n\nBy default it takes the first match in case there are multiple matching emojis. However if you append a dot (.) to a word you get to choose which emoji gets copied.\n\n### How to run it\n\n```\ngit clone git@github.com:bbelderbos/emojisearcher.git\ncd emojisearcher\npoetry install\npoetry run emo\n```\n\n(New to `poetry`? [Start here](https://python-poetry.org/docs/).)\n\nYou can also make a shell alias:\n\n```\n# .bashrc\nalias emo="cd $HOME/code/emojisearcher && poetry run emo"\n```\n\nAnd to run the tests:\n\n```\npoetry run pytest\n```\n\n### Other ways\n\nWhile sharing this on social media I learned about some useful OS shortcuts to retrieve emojis, [thanks Matt!](https://twitter.com/bbelderbos/status/1374414940988043264)\n',
    'author': 'Bob Belderbos',
    'author_email': 'bobbelderbos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bbelderbos/emojisearcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
