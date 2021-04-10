# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recurse_words']

package_data = \
{'': ['*']}

install_requires = \
['pygraphviz>=1.7,<2.0', 'requests>=2.25.1,<3.0.0', 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'recurse-words',
    'version': '0.2.0',
    'description': "find words that have other words in them that when you take the inner words out what's left is still a word",
    'long_description': "# recurse-words\nfind words that have other words in them that when you remove the inner word what's left is still a word\n\n![An example word tree of such a kind](examples/img/collaborationists.png)\n\n# installation\n\nFrom pypi:\n\n```\npip install recurse-words\n```\n\nFrom github:\n\n```\ngit clone https://github.com/sneakers-the-rat/recurse-words\npip install ./recurse-words\n# or\npoetry install ./recurse-words\n```\n\n# usage\n\nPoint the recurser at a file that has a list of words,\nfor example [this one](https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt), \nand let 'er rip\n\n```python\nfrom recurse_words import Recurser\n\nrecurser = Recurser('path/to/some/words.txt')\nrecurser.recurse_all_words()\nrecurser.save('word_trees.pck')\n\n# see word trees by a few metrics\n# max tree depth\nrecurser.by_depth\n# total number of leaves\nrecurser.by_leaves\n# total number of edges\nrecurser.by_density\n```\n\nDraw network graphs!\n\n```python\nrecurser.draw_graph('some_word', '/output/directory')\n```\n\nAuto-download different corpuses!\n\n```python\nrecurser = Recurser(corpus='english')\nrecurser = Recurser(corpus='phonetic')\n```\n\n",
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakers-the-rat/recurse-words',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
