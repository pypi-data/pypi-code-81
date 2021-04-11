# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pillaralgos', 'pillaralgos.helpers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0', 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'pillaralgos',
    'version': '1.0.7',
    'description': 'Algorithms for Pillar. Currently includes "mini" algorithms, nothing too sophisticated.',
    'long_description': '# Table of Contents\n1. [Build and Publish](#build)\n1. [Background](#background)\n   1. [Algorithms](#algorithms)\n      1. [Timeit Results](#timeit-results)\n   3. [Datasets](#datasets)\n3. [Current Goal](#current-goal)\n4. [Long Term Goal](#long-term-goal)\n\n# Build\nTo build and publish this package we are using the [poetry](https://python-poetry.org/) python packager. It takes care of some background stuff that led to mistakes in the past.\n\nFolder structure:\n```\n|-- pypi\n    |-- pillaralgos\n        |-- helpers\n            |-- __init__.py\n            |-- data_handler.py\n            |-- graph_helpers.py\n            |-- sanity_checks.py\n        |-- __init__.py  # must include version number\n        |-- algoXX.py\n    |-- LICENSE\n    |-- README.md\n    |-- pyproject.toml  # must include version number\n```\nTo publish just run the `poetry publish --build` command after update version numbers as needed.\n\n# Background\nPillar is creating an innovative way to automatically select and splice clips from Twitch videos for streamers. This repo is focusing on the algorithm aspect. Three main algorithms are being tested.\n\n## Algorithms\n\n1. [Algorithm 1](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_1.ipynb): Find the best moments in clips based on where the most users participated. Most is defined as the *ratio of unique users* during a 2 min section to unique users for the entire session.\n1. [Algorithm 2](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_2.ipynb) Find the best moments in clips based on when rate of messages per user peaked. This involves answering the question "at which 2 min segment do the most users send the most messages?". If users X, Y, and Z all send 60% of their messages at timestamp range delta, then that timestamp might qualify as a "best moment"\n   1. __NOTE__: Currently answers the question "at which 2 min segment do users send the most messages fastest"\n1. [Algorithm 3 (WIP)](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_3.ipynb) Weigh each user by their chat rate, account age, etc. Heavier users predicted to chat more often at "best moment" timestamps \n   1. __STATUS__: current weight determined by (`num_words_of_user`/`num_words_of_top_user`)\n   1. [Algorithm 3.5](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_3.5.ipynb) Finds the best moments in clips based on most number of words/emojis/both used in chat\n\n### Timeit results\nResults as of `4/11/21 12:21am EST`\n\n| algo1  | algo2        | algo3_0 | algo3_5 |\n|--------|--------------|---------|---------|\n|3.4 sec | 3 min 14 sec |39.4 sec | 28 sec  |\n\n## Datasets:\n1. Preliminary data `prelim_df`: 545 rows representing one 3 hour 35 minute 26 second twitch stream chat of [Hearthstone by LiiHS](https://www.twitch.tv/videos/963184458)\n    * Used to create initial json import and resulting df clean/merge function `organize_twitch_chat`\n2. Big data `big_df`: 2409 rows representing one 7 hour 37 minute, 0 second twitch stream chat of [Hearthstone by LiiHS](https://www.twitch.tv/videos/955629991)\n    * Used to create all algorithms\n\n# Current Goal\n\nTo create one overarching algorithm that will find the most "interesting" clips in a twitch VOD. This will be created through the following steps:\n1. Creation of various algorithms that isolate `min_` (2 by default) minute chunks. The basic workflow:\n   1. Create variable (ex: `num_words`, for number of words in the body of a chat message)\n   1. Group df by `min_` chunks, then average/sum/etc `num_words` for each `min_` chunks\n   1. Sort new df by `num_words`, from highest "value" to lowest "value"\n   1. Return this new df as json ([example](https://github.com/pomkos/twitch_chat_analysis/blob/main/exports/algo1_results.json))\n1. Users rate clips provided by each algorithm\n2. Useless algorithms thrown away\n3. Rest of the algorithms merged into one overarching algorithm, with weights distributed based on user ratings\n\n# Long Term Goal\n\n* __New objective measure__: community created clips (`ccc`) for a given VOD id with start/end timestamps for each clip\n* __Assumption__: `ccc` are interesting and can be used to create a narrative for each VOD. We can test this by cross referencing with posts to /r/livestreamfails upvotes/comments\n* __Hypothesis__: if we can predict where `ccc` would be created, those are potentially good clips to show the user\n   * *Short term test*: Create a model to predict where ccc would be created using variables such as word count, chat rate, emoji usage, chat semantic analysis. We can do this by finding timestamps of ccc and correlating them with chat stats\n   * *Medium term test*: Use top 100 streamers as training data. What similarities do their ccc and reddit most upvoted of that VOD share? (chat rate etc)\n      1. Get the transcript for these top 100\n      2. Get the top 100\'s YT posted 15-30min story content for the 8 hour VOD\n      3. Get the transcript for that story content\n      4. Semantic analysis and correlations, etc.\n   * *Long term test*: what percentage of clips do our streamers actually end up using\n',
    'author': 'Peter Gates',
    'author_email': 'pgate89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
