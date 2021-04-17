# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_todo']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-todo',
    'version': '0.1.5',
    'description': 'Simple ToDoList plugin for Nonebot',
    'long_description': '# Nonebot Plugin ToDo\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的待办事项提醒插件\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_todo)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-todo.svg)\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```\nnb plugin install nonebot_plugin_todo\n```\n\n- 使用 poetry\n\n```\npoetry add nonebot_plugin_todo\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_todo\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\ngit clone https://github.com/Jigsaw111/nonebot_plugin_todo.git\n```\n\n### 使用\n\n**不推荐使用此插件进行隐私相关的待办事项提醒！**\n\n**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为 `/` )。**\n\n- `todo list` 查看当前会话（群/私聊）的待办事项列表\n- `todo add job cron message` 新增待办事项（群聊仅管理员可用）\n- - `job` 作业名，每个会话不能存在两个相同的作业名\n- - `cron` crond 表达式，必须用 `""` 包裹，例如 `"* * * * *"` 表示每分钟\n- - `message` 要定时发送的消息，支持 CQ 码，必要时需用 `""` 包裹\n- `todo remove job` 删除待办事项\n- `todo pause job` 暂停待办事项\n- `todo resume job` 恢复待办事项\n\n### Q&A\n\n- **这是什么？**  \n  待办事项提醒，简称**闹钟**。\n- **有什么用？**  \n  **没有用**。这个项目不像 [nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager) 一样希望对他人有所帮助，只是我有个同学希望我每天晚上九点提醒他去跑步，就写了这玩意儿。\n\n<details>\n<summary>展开更多</summary>\n\n### Bug\n\n\n\n### Changelog\n\n- 210414，完成基本功能，发布 0.1.0 版本。\n- 210412，创建项目。\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_todo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
