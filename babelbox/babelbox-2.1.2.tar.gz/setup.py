# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['babelbox', 'babelbox.integration']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['babelbox = babelbox.__main__:app']}

setup_kwargs = {
    'name': 'babelbox',
    'version': '2.1.2',
    'description': 'A language localization generator for Minecraft',
    'long_description': '![](https://img.shields.io/github/license/orangeutan/babelbox)\n![](https://img.shields.io/badge/python-3.8|3.9-blue)\n[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)\n![](https://raw.githubusercontent.com/OrangeUtan/babelbox/cabe03f93500e0ee2e0bf9f39c03e52007989ecb/coverage.svg)\n![](https://img.shields.io/badge/mypy-checked-green)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/badge/pre--commit-enabled-green)\n![](https://github.com/orangeutan/babelbox/workflows/CI/badge.svg)\n\n# Babelbox\nBabelbox allows you to write your language files in .csv files and then generate Minecraft language.json files from them.<br>\nCreating translations in CSV gives you an easy overview over any errors or missing translations.<br>\n\n- [Installation](#Installation)\n- [Usage](#Usage)\n- [Getting started](#Getting-started)\n    - [Single file source](#Single-file-source)\n    - [Directory source](#Directory-source)\n    - [Shorten variable names](#Shorten-variable-names)\n    - [Organize translations in folders](#Organize-translations-in-folders)\n- [Beet plugin](#Beet-plugin)\n- [Contributing](#Contributing)\n- [Changelog](https://github.com/OrangeUtan/babelbox/blob/main/CHANGELOG.md)\n\n# Installation\n```shell\n$ pip install babelbox\n```\n\n# Usage\nReads translations from all sources and then generates minecraft language files for all language codes\n```shell\n$ # Single .csv file source\n$ babelbox <file.csv>\n$ # Directory containing .csv files as source\n$ babelbox <directory>\n$ # Multiple sources require output directory\n$ babelbox <file1.csv> <directory> <file2.csv> -o <output_dir>\n```\n\nAll options:\n```shell\n$ babelbox SOURCES...\n    -o, --out                   The output directory of the generated files\n    -p, --prefix-identifiers    Prefix identifiers with their path relative\n                                to their SOURCES entry\n    --dialect [excel|excel-tab|unix]\n                                CSV dialect used to parse CSV. Dialect will\n                                be automatically detected of omitted\n    -d, --delimiter             CSV delimiter overwrite\n    --quotechar                 CSV quote char overwrite\n    -m, --minify                Minify generated files\n    -i, --indent                Indentation used when generating files\n    --dry                       Dry run. Don not generate any files\n    -v, --verbose               Increase verbosity\n    -q, --quiet                 Only output errors\n```\n\n\n# Getting started\n## Single file source:\nWe have one `.csv` file containing translations:\n```\nresourcepack\n  ⠇\n  └╴lang\n    └╴ items.csv\n```\n\n| Item                                | en_us    | de_de      |\n| ----------------------------------- | -------- | ---------- |\n| item.stick.\ufeffname                   | stick    | Stock      |\n| # You can create comments like this |          |            |\n| item.snowball.\ufeffname                | snowball | Schneeball |\n\nPassing **items.csv** as a source to babelbox generates the language files **en_us.json** and **de_de.json**:\n```shell\n$ babelbox resourcepack/.../lang/items.csv\n```\n```json\nen_us.json\n{\n    "item.stick.name": "stick",\n    "item.snowball.name": "snowball",\n}\n\nde_de.json\n{\n    "item.stick.name": "Stock",\n    "item.snowball.name": "Schneeball",\n}\n```\n\n```\nresourcepack\n  ⠇\n  └╴lang\n    ├╴ items.csv\n    ├╴ en_us.json\n    └╴ de_de.json\n```\n\n## Directory source\nWe have two `.csv` files containing translations:\n```\nresourcepack\n  ⠇\n  └╴lang\n    ├╴ items.csv\n    └╴ blocks.csv\n```\n**items.csv**\n| Item                 | en_us    | de_de      |\n| -------------------- | -------- | ---------- |\n| item.stick.\ufeffname    | stick    | Stock      |\n\n**blocks.csv**\n| Block                 | en_us    | de_de     |\n| --------------------- | -------- | --------- |\n| block.log.\ufeffname      | log      | Holzstamm |\n\nPassing the **lang** directory as a source to babelbox generates the language files **en_us.json** and **de_de.json**:\n```shell\n$ babelbox resourcepack/.../lang\n```\n```json\nen_us.json\n{\n    "item.stick.name": "stick",\n    "block.log.name": "log",\n}\n\nde_de.json\n{\n    "item.stick.name": "Stock",\n    "block.log.name": "Holzstamm",\n}\n```\n```\nresourcepack\n  ⠇\n  └╴lang\n    ├╴ items.csv\n    ├╴ blocks.csv\n    ├╴ en_us.json\n    └╴ de_de.json\n```\n\n## Shorten variable names:\nWe can use the `--prefix-identifiers` flag to save ourselve some typing. If all identifiers share a common prefix, we can name the file to that prefix and let Babelbox prepend it.\n\n```\nresourcepack\n  ⠇\n  └╴lang\n    └╴ item.swords.csv\n```\n| Swords         | en_us         | de_de          |\n| -------------- | ------------- | -------------- |\n| diamond.\ufeffname | Diamond Sword | Diamantschwert |\n| gold.\ufeffname    | Gold sword    | Goldschwert    |\n\n```shell\n$ babelbox resourcepack/.../lang --prefix-identifiers\n$ # Or abbreviated\n$ babelbox resourcepack/.../lang -p\n```\n\n```json\nen_us.json\n{\n    "item.swords.diamond.name": "Diamond Sword",\n    "item.swords.gold.name": "Gold sword",\n}\n\nde_de.json\n{\n    "item.swords.diamond.name": "Diamantschwert",\n    "item.swords.gold.name": "Goldschwert",\n}\n```\n\nAll identifiers have been prefixed with `item.swords.`\n\n## Organize translations in folders\nWe can save ourselves even more typing and organize our translations files in a directory structure:\n\n```\nresourcepack\n  ⠇\n  └╴lang\n    ├╴ item\n    │  └╴ swords.csv\n    └╴ block\n      └╴ heavy.csv\n```\n**swords.csv**\n| Swords         | en_us         | de_de          |\n| -------------- | ------------- | -------------- |\n| gold.\ufeffname    | Gold sword    | Goldschwert    |\n\n**heavy.csv**\n| Heavy Blocks | en_us      | de_de       |\n| ------------ | ---------- | ----------- |\n| lead.\ufeffname  | Lead Block | Bleiblock |\n\n```shell\n$ babelbox resourcepack/.../lang -p\n```\n\n```json\nen_us.json\n{\n    "item.swords.gold.name": "Gold sword",\n    "block.heavy.lead.name": "Lead Block",\n}\n\nde_de.json\n{\n    "item.swords.gold.name": "Goldschwert",\n    "block.heavy.lead.name": "Bleiblock",\n}\n```\n```\nresourcepack\n  ⠇\n  └╴lang\n    ├╴ item\n    │  └╴ swords.csv\n    ├╴ block\n    │   └╴ heavy.csv\n    ├╴ en_us.json\n    └╴ de_de.json\n```\n\n# Beet plugin\nBabelbox can be used as a [`beet`](https://github.com/mcbeet/beet) plugin.\nHere is a example beet project using babelbox:\n```\nbeet.json\nresourcepack\n  ⠇\n  └╴lang\n    └╴item.swords.csv\n```\n**swords.csv**\n| Swords         | en_us         | de_de          |\n| -------------- | ------------- | -------------- |\n| gold.\ufeffname    | Gold sword    | Goldschwert    |\n\n**beet.json**\n```json\n{\n  "output": "build",\n  "resource_pack": {\n    "load": ["resourcepack"]\n  },\n  "pipeline": [\n      "babelbox.integration.beet"\n  ],\n  "meta": {\n      "babelbox": {\n          "load": ["resourcepack/assets/minecraft/lang"],\n          "prefix_identifiers": true\n      }\n  }\n}\n```\nRunning `beet build` generates the language files:\n```\nbeet.json\nresourcepack\n  ⠇\n  └╴lang\n    └╴item.swords.csv\nbuild\n  ⠇\n  └╴lang\n    ├╴en_us.json\n    └╴de_de.json\n```\n\n# Contributing\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org/). Setup dev environment with [`invoke`](http://www.pyinvoke.org/):\n```shell\n$ invoke install\n```\nRun tests:\n```shell\n$ invoke test\n```\nThe project follows [`black`](https://github.com/psf/black) codestyle. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/). Code formatting and type checking is enforced using [`pre-commit`](https://pre-commit.com/)\n',
    'author': 'Oran9eUtan',
    'author_email': 'Oran9eUtan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangeUtan/babelbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
