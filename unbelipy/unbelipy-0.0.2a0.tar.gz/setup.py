# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unbelipy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unbelipy',
    'version': '0.0.2a0',
    'description': "Asynchronous wrapper for UnbelievaBoat's API written in python",
    'long_description': '[![PyPI status](https://img.shields.io/pypi/status/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n[![PyPI version fury.io](https://badge.fury.io/py/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n[![PyPI license](https://img.shields.io/pypi/l/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n\n# unbelip\n\nAsynchronous wrapper for UnbelievaBoat\'s API written in python\n\n# Characteristics\n- Easy to use\n- Full error handling\n- Type hinted and readable code\n\n# Project status\nEarly alpha and as such unsuitable for production.\n\n# Installation\n\n`pip install unbelipy`\n\n# Use:\n\n```python\nfrom unbelipy import UnbeliClient\nimport asyncio\nTOKEN = "Token generated through Unbelievaboat\'s portal"\n\nclient = UnbeliClient(token=TOKEN)\n\nasync def main():\n    # get guild information\n    guild_info = await client.get_guild(guild_id=305129477627969547)\n    print(guild_info)\n    # get guild leaderboard\n    guild_leaderboard = await client.get_leaderboard(guild_id=305129477627969547)\n    print(guild_leaderboard)\n    # get user balance\n    balance = await client.get_balance(guild_id=305129477627969547, member_id=80821761460928512)\n    print(balance)\n    # put balance (set to x amount)\n    balance = await client.set_balance(guild_id=305129477627969547, \n                                       member_id=80821761460928512,\n                                       cash=1000,\n                                       reason="Showing off put method")\n    # patch balance (increment or decrement by x amount)\n    balance = await client.edit_balance(guild_id=305129477627969547, \n                                       member_id=80821761460928512,\n                                       cash=-500,\n                                       reason="Showing off patch method")\n    print(balance)\n\nasyncio.run(main())\n```\n\n"balance" is a returned Dataclass with balance information containing:\n- total: total amount of currency (cash + bank)\n- bank: amount in bank\n- cash: amount in cash\n- user_id: id of the user for which the amount is set\n- guild_id: id for the guild the user belongs to\n- rank: rank of the user in the guild according to query parameters\n\n"guild_info" is a dataclass with guild info containing:\n- id\n- name \n- icon\n- owner_id  \n- member_count  \n- symbol (currency)\n\nUnbeliClient also has a rate_limit_data attribute with information returned with each request from the API.\n\n\n',
    'author': 'chrisdewa',
    'author_email': 'alexdewa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisdewa/unbelipy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
