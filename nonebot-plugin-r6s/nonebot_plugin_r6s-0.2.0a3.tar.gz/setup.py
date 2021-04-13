# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_r6s']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.0,<0.18.0',
 'nonebot2>=2.0.0-alpha.10,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-r6s',
    'version': '0.2.0a3',
    'description': 'A R6s plugin for Nonebot2',
    'long_description': '<div align="center">\n\n# NoneBot Plugin R6s\n\nRainbow Six Siege Players Searcher For Nonebot2\n\n</div>\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/abrahum/nonebot-plugin-r6s/master/LICENSE">\n    <img src="https://img.shields.io/github/license/abrahum/nonebot_plugin_r6s.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-r6s">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-r6s.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方法\n\n``` zsh\nnb plugin install nonebot-plugin-r6s // or\npip install --upgrade nonebot-plugin-r6s\n```\n在 Nonebot2 入口文件（例如 bot.py ）增加：\n``` python\nnonebot.load_plugin("nonebot_plugin_r6s")\n```\n\n## 指令详解\n\n|指令|别名|可接受参数|功能|\n|:-:|:-:|--|---|\n|r6s|彩六，彩虹六号，r6，R6|昵称|查询玩家基本信息|\n|r6spro|r6pro，R6pro|昵称|查询玩家进阶信息|\n|r6sops|r6ops，R6ops|昵称|查询玩家干员信息|\n|r6sp|r6p，R6p|昵称|查询玩家近期对战信息|\n|r6sset|r6set，R6set|昵称|设置玩家昵称，设置后其余指令可以不带昵称即查询已设置昵称信息|\n\n## 更新日志\n\n### 0.2.0-alpha.1\n\n- 更换优先使用 ground 数据源，cn 数据源存在排位休闲数据错位，改名后数据长期未更新问题。\n- ground 数据源乱码严重，目前无法识别干员数据和近期对战数据\n- 已知 ground 数据源第一次使用会返回未更新数据，待研究解决（咕咕咕）\n\n### 0.2.0-alpha.2\n\n- 针对有 Ubi 账号未游玩 R6s 账号返回 Not Found\n\n## 特别鸣谢\n\n[nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架\n\n[Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的 [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现\n\n',
    'author': 'abrahumlink',
    'author_email': '307887491@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahum/nonebot_plugin_r6s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
