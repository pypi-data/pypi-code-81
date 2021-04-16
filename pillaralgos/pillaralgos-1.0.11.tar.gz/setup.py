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
    'version': '1.0.11',
    'description': 'Algorithms for Pillar. Currently includes "mini" algorithms, nothing too sophisticated.',
    'long_description': 'NOTE: This readme is just a quick reference. For more details include todo, near/medium/long term goals please see our GitHub page.\n\n# Table of Contents\n1. [Use](#use)\n   1. [Input variables](#input-variables)\n   2. [Output variables](#output-variables)\n2. [Background](#background)\n   1. [Algorithms](#algorithms)\n   1. [Timeit Results](#timeit-results)\n3. [Build and Publis](#build)\n4. [Changelog](#changelog)\n\n# Use\n\nTo use any of the algorithms just import as needed with `from pillaralgos import algo1`, and then `algo1(data, min_=2, save_json=False)`.\n\n## Input variables\n\n```\nsave_json: bool\n    True if want to save results as json to exports folder\ndata: list\nmin_: int\n    Approximate number of minutes each clip should be\nsort_by: str\n    For algo1 ONLY\n    \'rel\': "number of chatters at timestamp"/"number of chatters at that hour"\n    \'abs\': "number of chatters at timestamp"/"total number of chatters in stream"\ngoal: str\n    For algo3_5 ONLY\n    \'num_words\': sum of the number of words in each chat message\n    \'num_emo\': sum of the number of emoticons in each chat message\n    \'num_words_emo\': sum of the number of words + emoticons in each chat message\nmin_words:int\n    For algo3_0 ONLY\n    When filtering chunks to top users, at least how many words the top user should send\n```\n\n## Output variables\n\n* All algorithms will return a `result_json`, list of dictionaries in the format of `{start:seconds, end:seconds}` where `seconds` is seconds elapsed since start of the stream. List is ordered from predicted best to worst timestamps.\n* All algorithms can save the returned list as a .json if `save_json=True` is passed in.\n\n# Background\nPillar is creating an innovative way to automatically select and splice clips from Twitch videos for streamers. This repo is focusing on the algorithm aspect. Three main algorithms are being tested.\n\n## Algorithms\n\n1. [Algorithm 1](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_1.ipynb): Find the best moments in clips based on where the most users participated. Most is defined as the *ratio of unique users* during a 2 min section to unique users for the entire session.\n1. [Algorithm 2](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_2.ipynb) Find the best moments in clips based on when rate of messages per user peaked. This involves answering the question "at which 2 min segment do the most users send the most messages?". If users X, Y, and Z all send 60% of their messages at timestamp range delta, then that timestamp might qualify as a "best moment"\n   1. __NOTE__: Currently answers the question "at which 2 min segment do users send the most messages fastest"\n1. [Algorithm 3 (WIP)](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_3.ipynb) Weigh each user by their chat rate, account age, etc. Heavier users predicted to chat more often at "best moment" timestamps \n   1. __STATUS__: current weight determined by (`num_words_of_user`/`num_words_of_top_user`)\n   1. [Algorithm 3.5](https://github.com/pomkos/twitch_chat_analysis/blob/reorganize_repo/algorithm_3.5.ipynb) Finds the best moments in clips based on most number of words/emojis/both used in chat\n\n### Timeit results\nResults as of `April 13, 2021 18:31 EST` run on `big_df` with 80841 rows, 10 columns.\n\n| algo1  | algo2        | algo3_0 | algo3_5 |\n|--------|--------------|---------|---------|\n|2.2 sec | 1 min 23 sec |28.1 sec | 16.3 sec|\n\n# Build\nTo build and publish this package we are using the [poetry](https://python-poetry.org/) python packager. It takes care of some background stuff that led to [mistakes in the past](https://github.com/pillargg/twitch_chat_analysis/issues/8).\n\nFolder structure:\n```\n|-- pypi\n    |-- pillaralgos  # <---- note that poetry didn\'t require an additional subfolder\n        |-- helpers\n            |-- __init__.py\n            |-- data_handler.py\n            |-- graph_helpers.py\n            |-- sanity_checks.py\n        |-- __init__.py  # must include version number\n        |-- algoXX.py  # all algorithms in separate files\n    |-- LICENSE\n    |-- README.md\n    |-- pyproject.toml  # must include version number\n```\nTo publish just run the `poetry publish --build` command after update version numbers as needed.\n\n# Changelog\n\n* Moved `dev` and `prod` folders out of `pypi` folder for ease of access\n* New licensing\n* Added unit tests, sample data, sample answers (#6, #17, #18)\n* Fixed use of iloc vs loc (#20)\n* Algos2,3_0,3_5 now properly outputs correct lengths based on param input (#15, #21, #31)\n* Algos return empty numpy array if no results found\n* Created `brain.run()` that runs all algos and then returns common timestamps amongst them. See `help(brain)` and `help(brain.run` for more info\n* Removed some old notebooks, moved some code to `archive.ipynb`',
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
