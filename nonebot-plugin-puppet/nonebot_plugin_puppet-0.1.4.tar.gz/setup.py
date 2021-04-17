# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_puppet']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-puppet',
    'version': '0.1.4',
    'description': 'Make Nonebot your puppet',
    'long_description': '# Nonebot Plugin Puppet\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的会话转接插件\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_puppet)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-puppet.svg)\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n<!--\n- 使用 nb-cli  \n\n```\nnb plugin install nonebot_plugin_puppet\n```\n-->\n\n- 使用 poetry\n\n```\npoetry add nonebot_plugin_puppet\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_puppet\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\ngit clone https://github.com/Jigsaw111/nonebot_plugin_puppet.git\n```\n\n### 使用\n\n**仅限超级用户私聊使用**\n\n- `puppet link` 链接会话\n- - `-u user_id, --user user_id` 可选参数，指定链接会话的 QQ 号\n- - `-g group_id, --group group_id` 可选参数，指定链接会话的群号\n- `puppet send message` 向链接会话发送消息，用于发送已被占用的指令\n- - `message` 需要发送消息，如有空格请用 `""` 包裹\n- `puppet unlink` 取消链接会话\n\n### Q&A\n\n- **这是什么？**  \n  会话转接，让 Nonebot 成为你的傀儡。\n- **有什么用？**  \n  **没有用**。\n\n<details>\n<summary>展开更多</summary>\n\n### Bug\n\n- [ ] 不允许多个超级用户链接到同一会话\n\n### Changelog\n\n- 210416，创建项目。\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_puppet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
