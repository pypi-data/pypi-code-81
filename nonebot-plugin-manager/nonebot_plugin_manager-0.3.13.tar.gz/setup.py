# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_manager']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-manager',
    'version': '0.3.13',
    'description': 'Nonebot Plugin Manager base on import hook',
    'long_description': '<div align="center">\n\t<img width="200" src="docs/logo.png" alt="logo"></br>\n\n# Nonebot Plugin Manager\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的**非侵入式**插件管理器\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)\n\n</div>\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```bash\nnb plugin install nonebot_plugin_manager\n```\n\n- 使用 poetry\n\n```bash\npoetry add nonebot_plugin_manager\n```\n\n- 使用 pip\n\n```bash\npip install nonebot_plugin_manager\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```bash\ngit clone https://github.com/Jigsaw111/nonebot_plugin_manager.git\n```\n\n### 使用\n\n**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为 `/` )。**\n\n- `npm list` 查看当前群插件列表\n- - `-s, --store` 可选参数，查看 Nonebot 插件商店（仅超级用户可用）\n- - `-d, --default` 可选参数，管理默认设置（仅超级用户可用）\n- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）\n\n- `npm block 插件名...` 屏蔽当前群插件 （仅群管及超级用户可用）\n- - `-a, --all` 可选参数，全选插件\n- - `-d, --default` 可选参数，管理默认设置 （仅超级用户可用）\n- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）\n\n- `npm unblock 插件名...` 启用当前群插件 （仅群管及超级用户可用）\n- - `-a, --all` 可选参数，全选插件\n- - `-d, --default` 可选参数，管理默认设置 （仅超级用户可用）\n- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）\n\n- `npm info 插件名` 查询插件信息 （仅超级用户可用）\n\n*以下功能尚未实现*\n\n- `npm install 插件名...` 安装插件 （仅超级用户可用）\n- - `-i index, --index index` 指定 PyPI 源\n\n- `npm update 插件名...` 更新插件 （仅超级用户可用）\n- - `-i index, --index index` 指定 PyPI 源\n- - `-a, --all` 可选参数，全选插件\n\n- `npm uninstall 插件名...` 卸载插件 （仅超级用户可用）\n- - `-a, --all` 可选参数，全选插件\n\n### 导出\n\n```python\nfrom nonebot import require\n\nexport = require("nonebot_plugin_manager")\n\n# 在指定群聊中启用/禁用插件\nexport.block_plugin(group_id, *plugins)\nexport.unblock_plugin(group_id, *plugins)\n# 获取指定群插件列表\nexport.get_group_plugin_list(group_id)\n```\n\n### Q&A\n\n- **这是什么？**  \n  基于 import hook 的插件管理器，能够在不重启 nonebot2 的情况下分群管理插件。\n- **有什么用？**  \n  在 nonebot2 仍然缺乏插件管理机制的时期暂时充当插件管理器。\n- **自造 Rule 不是更好？**  \n  Rule 当然更好且更有效率，但是 Rule 是一种**侵入式**的插件管理方式，需要用户自行修改其他插件，这对于管理从 pypi 安装的插件来说相对复杂。而使用本插件，你不需要修改其他插件的任何内容，更符合插件之间**松耦合**的设计原则。\n\n### Thanks\n\n[nonebot/nb-cli](https://github.com/nonebot/nb-cli)\n\n\n<details>\n<summary>展开更多</summary>\n\n### 原理\n\n使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。\n\n事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。\n\n*以下功能尚未实现*\n\n当然，你也可以使用 `npm uninstall` 命令来真正卸载插件，但我不建议你这样做，因为该命令将会重启 Nonebot 。\n\n### TO DO\n\n- [x] 分群插件管理\n- [ ] 安装卸载插件\n\n### Bug\n\n- [ ] 无法停用 Matcher 以外的机器人行为（如 APSchedule ）  \n      **解决方法：** 暂无\n- [x] 任何人都可以屏蔽/启用插件\n- [ ] 如果加载了内置插件将会导致错误  \n      **解决方法：** 问低调佬\n\n### Changelog\n\n- 210415，不再将没有 Matcher 的插件添加到插件列表。\n- 210403，分离默认设置与私聊设置，默认设置的键值改为 `default`。\n- 210402，修复 nonebot 2.0.0a13 更新导致的 bug。\n- 210331，添加 logo。\n- 210330，修复禁用/启用颠倒的 bug。\n- 210329，修复 block/unblock 指令中的 -a 参数无效的 bug，修复文档中导出部分的错误。\n- 210320，新增 `get_group_plugin_list` 的 export 用于获取群插件列表。\n- 210317，调整项目结构，将绝大多数数据处理操作移至 data，handle 只负责调用；修改 export，不再对其他插件暴露底层接口。\n- 210314，修复 `npm list`  的 --group 参数不起作用的 bug，实现查询插件信息。\n- 210313，实现爬取插件商店列表，实现 -h 参数，新增 export 导出给其他插件。\n- 210312，重构 0.3.0，`setting.json` 重命名为 `plugin_list.json`，结构改为 `plugin:{group_id:true,group_id:false}`。\n- 210310，0.3.0 完工，将__init__.py分离成 setting,command,nb 三个文件。\n- 210310，0.2.0 完工，命令格式改为 shelllike，使用 `setting.json` 作为配置文件，基本结构为 `group_id:{plugin:true,plugin:false}` 。\n- 210307，0.1.0 完工，上架插件商店。确定了通过 `run_preprocessor` 屏蔽 Matcher 的基本原理，使用 `block_list` 作为全局设置（即只屏蔽 block_list 中的插件）\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
