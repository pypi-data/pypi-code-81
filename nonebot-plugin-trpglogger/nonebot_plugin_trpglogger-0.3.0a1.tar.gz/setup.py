# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_trpglogger']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.13,<2.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

extras_require = \
{'mah': ['nonebot-adapter-mirai>=2.0.0-alpha.11.post2,<3.0.0']}

setup_kwargs = {
    'name': 'nonebot-plugin-trpglogger',
    'version': '0.3.0a1',
    'description': 'a logger for TRPG',
    'long_description': '# TRPG Logger\n\n*基于 [nonebot2](https://github.com/nonebot/nonebot2)，兼容 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 和 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 的 QQ 跑团记录记录器*\n\n[![License](https://img.shields.io/github/license/thereisnodice/TRPGLogger)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0.a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-trpglogger.svg)\n\n用来记录跑团记录的 nonebot2 插件，与 https://logpainter.kokona.tech 配合使用。\n\n*移植自 [Dice-Developer-Team/TrpgLogger](https://github.com/Dice-Developer-Team/TrpgLogger)*\n\n### 安装\n\n* 使用nb-cli（推荐）  \n\n```bash\nnb plugin install nonebot_plugin_trpglogger\n```\n\n* 使用poetry\n\n```bash\npoetry add nonebot_plugin_trpglogger\n```\n\n### 开始使用\n\n`.log on` 开始记录\n\n`.log off` 停止记录\n\n**一个群同一时间段不能存在两个记录！**\n\n### TO DO\n\n- [ ] 暂停记录\n- [ ] 多开记录\n\n<details>\n<summary>展开更多</summary>\n\n### 原理\n\n与 [TrpgLogger](https://github.com/Dice-Developer-Team/TrpgLogger)* 一样，使用 AWS S3 进行储存（目前为了与 Logpainter 对接，是直接用溯洄的公共 bucket ）。\n\n### Bug\n\n- [x] go-cqhttp 无法记录机器人本身发出的消息（即无法记录掷骰）  \n    **请确保 go-cqhttp 的 `enable_self_message` 设置为 true**\n- [ ] mirai-api-http 无法记录机器人本身发出的消息（即无法记录掷骰）  \n    **由于 mirai-api-http 没有 `message_sent` 事件，所以该 bug 暂时无法解决。**\n- [ ] 在记录时间超过 24 小时后，如果上传文件失败会阻塞线程  \n    **如何解决:** 待定\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thereisnodice/TRPGLogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
