# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pancakeswap_lottery']

package_data = \
{'': ['*'], 'pancakeswap_lottery': ['assets/*']}

install_requires = \
['web3>=5.18.0,<6.0.0']

setup_kwargs = {
    'name': 'pancakeswap-lottery',
    'version': '0.1.4',
    'description': 'A Python client for accessing PancakeSwap Lottery smart contract information through Web3.py',
    'long_description': '# PancakeSwap Lottery 🥞 - Web3 client\n\n[![PyPI version](https://badge.fury.io/py/pancakeswap-lottery.svg)](https://badge.fury.io/py/pancakeswap-lottery)\n![PyPI downloads](https://img.shields.io/pypi/dm/pancakeswap-lottery)\n![Licence](https://img.shields.io/github/license/frefrik/pancakeswap-lottery)\n![Python version](https://img.shields.io/pypi/pyversions/pancakeswap-lottery)\n\nA Python client for accessing [PancakeSwap Lottery](https://pancakeswap.finance/lottery) smart contract information through [Web3.py](https://github.com/ethereum/web3.py).\n\n## Installation\nInstall from [PyPI](https://pypi.org/project/pancakeswap-lottery/):\n```\npip install pancakeswap-lottery\n```\n\n## Usage\n```python\nfrom pancakeswap_lottery import Lottery\n\nlottery = Lottery()\n\n# Current lottery round\nissue_index = lottery.get_issue_index()\n\n# Total pot (CAKE) of current lottery round\ntotal_amount = lottery.get_total_amount()\n\n# Prize pool allocation (percent)\nallocation = lottery.get_allocation()\n\n# Total addresses\ntotal_addresses = lottery.get_total_addresses()\n\n# Drawed \ndrawed = lottery.get_drawed()\n\n# Drawing phase\ndrawing_phase = lottery.get_drawing_phase()\n\n# Last timestamp\ntimestamp = lottery.get_last_timestamp(epoch=False)\n\n# Date and time of lottery round\nlottery_date = lottery.get_lottery_date(432)\n\n# Total rewards of lottery round\ntotal_rewards = lottery.get_total_rewards(432)\n\n# Winning numbers of lottery round\nhistory_numbers = lottery.get_history_numbers(432)\n\n# Numbers of tickets matched\nhistory_amount = lottery.get_history_amount(432)\n\n# Numers of tickets matched a specified number\nmatching_reward_amount = lottery.get_matching_reward_amount(432, 3)\n\n# Lottery numbers for a given ticket\nlottery_numbers = lottery.get_lottery_numbers(1328060)\n\n# Rewards for a given ticket\nreward_view = lottery.get_reward_view(1328060)\n\n# Max number\nmax_number = lottery.get_max_number()\n\n# CAKE contract address\ncake_contract = lottery.get_cake()\n\n# PLT-token contract address\nlottery_contract = lottery.get_lotteryNFT()\n\n# Total number of tickets bought by a given address\nbalance = lottery.get_balance_of("0xc13456A34305e9265E907F70f76B1BA6E2055c8B")\n```\n\n### Response previews\n```python\n>>> lottery.get_issue_index()\n435\n\n>>> lottery.get_total_amount()\n34977.25\n\n>>> lottery.get_allocation()\n{\'1\': 50, \'2\': 20, \'3\': 10}\n\n>>> lottery.get_total_addresses()\n200\n\n>>> lottery.get_drawed()\nFalse\n\n>>> lottery.get_drawing_phase()\nFalse\n\n>>> lottery.get_last_timestamp(epoch=False)\n2021-03-27 11:38:49\n\n>>> lottery.get_lottery_date(432)\n2021-03-26 02:00:00+00:00\n\n>>> lottery.get_total_rewards(432)\n51384.125\n\n>>> lottery.get_history_numbers(432)\n[2, 13, 7, 3]\n\n>>> lottery.get_history_amount(432)\n{\'4\': 1, \'3\': 34, \'2\': 718}\n\n>>> lottery.get_matching_reward_amount(432, 3)\n34\n\n>>> lottery.get_lottery_numbers(1328060)\n[11, 5, 14, 6]\n\n>>> lottery.get_reward_view(1328060)\n0\n\n>>> lottery.get_max_number()\n14\n\n>>> lottery.get_min_price()\n1\n\n>>> lottery.get_cake()\n0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82\n\n>>> lottery.get_lotteryNFT()\n0x5e74094Cd416f55179DBd0E45b1a8ED030e396A1\n\n>>> lottery.get_balance_of("0xc13456A34305e9265E907F70f76B1BA6E2055c8B")\n2673\n```\n\n## Donate\nIf you found this library useful and want to support my work feel free to donate a small amount 🙏🏻\n\n- 🥞 CAKE: 0xCFad66049e2C9Bc28647B2e2e3449B6B7C602d42\n- Ξ ETH: 0x7E916c46157f012Fb8dece4A042Dc603e8d627Df\n- ₿ BTC: bc1qgn2mdf5wsxft33s3ea8sh060y85mzntzs8cuu7\n',
    'author': 'Fredrik Haarstad',
    'author_email': 'codemonkey@zomg.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frefrik/pancakeswap-lottery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
